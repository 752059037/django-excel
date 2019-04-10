from django.db import models


# Create your models here.


# class bx_everyday_contrast_data(models.Model):
#     brand_id = models.IntegerField(max_length=20)
#     parent_grade_id = models.IntegerField(null=True, default=None)
#     id = models.AutoField(max_length=20, primary_key=True)
#     grade_id = models.IntegerField()
#     name = models.CharField(max_length=255)
#     include_num_contrast = models.FloatField()
#     arrival_num_contrast = models.FloatField(max_length=(20, 2))
#     stay_num_contrast = models.FloatField(max_length=(20, 2))
#     arrival_rate_contrast = models.FloatField(max_length=(20, 2))
#     stay_rate_contrast = models.FloatField(max_length=(20, 2))
#     month_id = models.IntegerField()


class BxEverydayContrastData(models.Model):
    brand_id = models.IntegerField()
    parent_grade_id = models.IntegerField(blank=True, null=True)
    grade_id = models.IntegerField()
    name = models.CharField(max_length=255)
    include_num_contrast = models.FloatField()
    arrival_num_contrast = models.FloatField()
    stay_num_contrast = models.FloatField()
    arrival_rate_contrast = models.FloatField()
    stay_rate_contrast = models.FloatField()
    month_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bx_everyday_contrast_data'
