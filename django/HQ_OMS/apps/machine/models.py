# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Machine(models.Model):
    process_equipment_code = models.CharField(primary_key=True, max_length=50, db_comment='工序设备编码')
    city = models.CharField(max_length=30, blank=True, null=True, db_comment='城市')
    category = models.CharField(max_length=30, blank=True, null=True, db_comment='类别')
    sub_category = models.CharField(max_length=50, blank=True, null=True, db_comment='子类')
    unit = models.CharField(max_length=50, blank=True, null=True, db_comment='单位')
    supplier = models.CharField(max_length=100, blank=True, null=True, db_comment='所属供应商')
    detailed_model = models.CharField(max_length=100, blank=True, null=True, db_comment='详细型号')
    serial_number = models.CharField(max_length=50, blank=True, null=True, db_comment='序列号')
    internal_external_distinction = models.CharField(max_length=20, blank=True, null=True, db_comment='内外部区分')
    machine_configuration = models.CharField(max_length=200, blank=True, null=True, db_comment='机台配置')
    price = models.CharField(max_length=30, blank=True, null=True, db_comment='价格')
    preset_price_before_tax = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True, db_comment='机台预设价格(￥/分钟)(未税)')
    current_user = models.CharField(max_length=50, blank=True, null=True, db_comment='正在使用人员')
    project_start_time = models.DateTimeField(blank=True, null=True, db_comment='项目开始时间')
    usage_status = models.CharField(max_length=100, blank=True, null=True, db_comment='使用情况')
    remark = models.CharField(max_length=100, blank=True, null=True, db_comment='备注')
    preset_price_after_tax = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True, db_comment='机台预设价格(￥/分钟)(含税)')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, db_comment='税率')

    class Meta:
        managed = False
        db_table = 'machine'
        db_table_comment = '机台列表相关信息表'


class MachineUsageRecord(models.Model):
    record_id = models.AutoField(primary_key=True, db_comment='记录编号')
    machine_name = models.CharField(max_length=50, blank=True, null=True, db_comment='机台')
    usage_type = models.CharField(max_length=30, blank=True, null=True, db_comment='使用类型')
    start_time = models.DateTimeField(blank=True, null=True, db_comment='开始时间')
    duration_minutes = models.IntegerField(blank=True, null=True, db_comment='耗时(min)')
    end_time = models.DateTimeField(blank=True, null=True, db_comment='结束时间')
    creator_name = models.CharField(max_length=20, blank=True, null=True, db_comment='创建人')
    creation_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    device_code = models.CharField(max_length=20, blank=True, null=True, db_comment='设备编码')

    class Meta:
        managed = False
        db_table = 'machine_usage_record'
        db_table_comment = '机台耗时记录表'


class MachineExternal(models.Model):
    process_equipment_code = models.CharField(primary_key=True, max_length=50, db_comment='工序设备编码')
    city = models.CharField(max_length=30, blank=True, null=True, db_comment='城市')
    category = models.CharField(max_length=30, blank=True, null=True, db_comment='类别')
    sub_category = models.CharField(max_length=50, blank=True, null=True, db_comment='子类')
    unit = models.CharField(max_length=50, blank=True, null=True, db_comment='单位')
    supplier = models.CharField(max_length=100, blank=True, null=True, db_comment='所属供应商')
    detailed_model = models.CharField(max_length=100, blank=True, null=True, db_comment='详细型号')
    serial_number = models.CharField(max_length=50, blank=True, null=True, db_comment='序列号')
    internal_external_distinction = models.CharField(max_length=20, blank=True, null=True, db_comment='内外部区分')
    machine_configuration = models.CharField(max_length=200, blank=True, null=True, db_comment='机台配置')
    price = models.CharField(max_length=30, blank=True, null=True, db_comment='价格')
    preset_price_before_tax = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True, db_comment='机台预设价格(￥/分钟)(未税)')
    current_user = models.CharField(max_length=50, blank=True, null=True, db_comment='正在使用人员')
    project_start_time = models.DateTimeField(blank=True, null=True, db_comment='项目开始时间')
    usage_status = models.CharField(max_length=100, blank=True, null=True, db_comment='使用情况')
    remark = models.CharField(max_length=100, blank=True, null=True, db_comment='备注')
    preset_price_after_tax = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True, db_comment='机台预设价格(￥/分钟)(含税)')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, db_comment='税率')

    class Meta:
        managed = False
        db_table = 'machine_external'
        db_table_comment = '机台列表(外部)'
