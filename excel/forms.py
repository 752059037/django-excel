# 创建人;Ye
# 创建时间 : 19.4.9  14:37

from django import forms
from excel import models


class BxEverydayContrastData_form(forms.ModelForm):
    # def clean(self):
    #     print(self.cleaned_data)
        
    class Meta:
        model = models.BxEverydayContrastData
        fields = "__all__"
