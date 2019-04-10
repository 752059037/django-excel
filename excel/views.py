from django.shortcuts import render
from django import views
import xlrd
from excel import models
from django.db import transaction
from excel.forms import BxEverydayContrastData_form
import logging
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt=' %Y-%m-%d %H:%M:%S')


# Create your views here.

class Import_Excel(views.View):
    def get(self, request):
        return render(request, 'import_excel.html')
    
    def post(self, request):
        
        xlsx = request.FILES.get('xlsx')
        if xlsx:
            file_formats = xlsx.name.split('.')[-1]
            if file_formats == 'xlsx':
                file_name = xlsx.name
                file_save_path = 'files/{}'.format(file_name)
                with open(file_save_path, 'wb') as f:
                    for line in xlsx.chunks():
                        f.write(line)  # 将接收到的xlsx文件写入到/files/文件夹下
                xlsx_obj = Operation_xlsx(file_save_path)
                xlsx_iter = xlsx_obj.read_xlsx()  # 生成器读取excel每一行
                ret = xlsx_obj.verity_save_xlsx(xlsx_iter)  # 校验并保存到数据库,返回错误信息
                xlsx_obj.del_xlsx()   # 删除接收的xlsx文件
            else:
                ret = {'code': 0, 'msg': [{'文件错误': ['请传入正确文件']}]}
        else:
            ret = {'code': 0, 'msg': [{'文件错误': ['请传入文件']}]}
        return render(request, 'import_excel.html', {'ret': ret})


class Operation_xlsx:
    """
    操作excel表格的类
    传入excel表格的路径

    """
    
    def __init__(self, path):
        self.path = path
        self.data = xlrd.open_workbook(self.path)
    
    def read_xlsx(self):
        """
        :return: 返回生成器,包含[页数,行数,内容]
        """
        sheets = self.data.sheets()
        for sheet in sheets:
            nrows = sheet.nrows
            for i in range(1, nrows):
                yield [sheet.name, i + 1, sheet.row_values(i)]
    
    @staticmethod
    def verity_save_xlsx(xlsx_iter):
        """
        :param xlsx_iter: 生成器对象或可迭代对象
        :return: 返回错误信息
        """
        ret = {'code': 1, 'msg': []}
        try:
            with transaction.atomic():  # 开启事务 如果出错则全部不保存
                for i in xlsx_iter:  # 循环得到excel里的每行数据
                    page_number = i[0]
                    line_number = i[1]
                    content = i[2]
                    if len(content) != 10:  # 判断表格字段长度是否正确
                        ret['msg'].append({'{}页 第{}行'.format(page_number, line_number, ): ['数据长度错误', ]})
                        continue
                    
                    form_obj = BxEverydayContrastData_form(  # 创建form对象用于校验数据
                        {
                            'brand_id': content[0],
                            'parent_grade_id': content[1],
                            'grade_id': content[2],
                            'name': content[3],
                            'include_num_contrast': content[4],
                            'arrival_num_contrast': content[5],
                            'stay_num_contrast': content[6],
                            'arrival_rate_contrast': content[7],
                            'stay_rate_contrast': content[8],
                            'month_id': content[9],
                        }
                    )
                    if form_obj.is_valid():  # 如果数据正确,按照brand_id 有则更新 无则创建
                        models.BxEverydayContrastData.objects.update_or_create(
                            brand_id=form_obj.cleaned_data.get('brand_id'),
                            defaults=form_obj.cleaned_data
                        )
                    else:
                        error_data, error_msg = list(form_obj.errors.items())[0]
                        ret['msg'].append({'{}页 第{}行,{}'.format(page_number, line_number, error_data, ): error_msg})
                if ret['msg']:
                    ret['code'] = 0
                    
                    raise ValueError('表格出现异常,执行回滚')
        except Exception as e:
            logging.error(e)
        return ret

    def del_xlsx(self):
        """
        删除接收到的xlsx文件
        :return:
        """
        os.remove(self.path)
