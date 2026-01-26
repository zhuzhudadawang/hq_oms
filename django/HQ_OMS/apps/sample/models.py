# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Sample(models.Model):
    order_id = models.CharField(max_length=30, blank=True, null=True, db_comment='关联订单')
    customer_sample_id = models.CharField(max_length=50, blank=True, null=True, db_comment='客户样点编号')
    customer_name = models.CharField(max_length=30, blank=True, null=True, db_comment='客户名')
    test_project = models.CharField(max_length=30, blank=True, null=True, db_comment='检测项目')
    receive_time = models.DateTimeField(blank=True, null=True, db_comment='接收时间')
    sender = models.CharField(max_length=20, blank=True, null=True, db_comment='送件人')
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True, db_comment='状态')  # Field name made lowercase.
    slice_position = models.CharField(max_length=50, blank=True, null=True, db_comment='切片位置')
    case_analysis_project_type = models.CharField(max_length=30, blank=True, null=True, db_comment='案件分析项目类型')
    process_status = models.CharField(max_length=20, blank=True, null=True, db_comment='工序状态')
    sample_quantity = models.IntegerField(blank=True, null=True, db_comment='样品数量')
    sample_validity_hours = models.IntegerField(blank=True, null=True, db_comment='样点时效(h)')
    last_process_step = models.CharField(max_length=50, blank=True, null=True, db_comment='最后工艺步骤')
    sample_preparation_direction = models.CharField(max_length=50, blank=True, null=True, db_comment='制样方向')
    task_assignee = models.CharField(max_length=20, blank=True, null=True, db_comment='任务分配人')
    notes = models.CharField(max_length=50, blank=True, null=True, db_comment='注意事项')
    main_attention_info = models.CharField(max_length=50, blank=True, null=True, db_comment='主要关注信息')
    reviewer = models.CharField(max_length=20, blank=True, null=True, db_comment='审核人')
    test_start_time = models.DateTimeField(blank=True, null=True, db_comment='检测开始时间')
    test_completion_time = models.DateTimeField(blank=True, null=True, db_comment='检测完成时间')
    task_assignment_time = models.DateTimeField(blank=True, null=True, db_comment='任务分配时间')
    expected_time_minutes = models.IntegerField(blank=True, null=True, db_comment='期望用时（分钟）')
    expected_completion_time = models.DateTimeField(blank=True, null=True, db_comment='期望完成时间')
    order_status = models.CharField(max_length=20, blank=True, null=True, db_comment='订单状态')
    sample_box_location = models.CharField(max_length=20, blank=True, null=True, db_comment='存放样点盒')
    execution_plan_file = models.CharField(max_length=50, blank=True, null=True, db_comment='执行方案（文件）')
    sample_id = models.CharField(primary_key=True, max_length=30, db_comment='样点编号')
    execution_plan = models.CharField(max_length=50, blank=True, null=True, db_comment='执行方案')
    base_material = models.CharField(max_length=50, blank=True, null=True, db_comment='基底材料')
    e_beam = models.CharField(max_length=50, blank=True, null=True, db_comment='E - beam')
    sample_materials = models.CharField(max_length=50, blank=True, null=True, db_comment='样品所含材质')
    sample_confirmation_date = models.DateTimeField(blank=True, null=True, db_comment='样点确认日期')
    sample_confirmation_time = models.DateTimeField(blank=True, null=True, db_comment='样点确认时间')
    order_status_duplicated = models.CharField(max_length=20, blank=True, null=True, db_comment='订单状态')
    packaging_form = models.CharField(max_length=20, blank=True, null=True, db_comment='封装形式')
    project_category = models.CharField(max_length=20, blank=True, null=True, db_comment='项目分类')
    related_customer = models.CharField(max_length=30, blank=True, null=True, db_comment='关联客户')
    validity_start_date = models.DateTimeField(blank=True, null=True, db_comment='时效起算日期')
    validity_start_time = models.TimeField(blank=True, null=True, db_comment='时效起算时间')
    sample_holder = models.CharField(max_length=20, blank=True, null=True, db_comment='样点持有人')
    delivery_date = models.DateTimeField(blank=True, null=True, db_comment='交期日期')
    delivery_time = models.TimeField(blank=True, null=True, db_comment='交期时间')
    lot_wafer_sample_id = models.CharField(max_length=50, blank=True, null=True, db_comment='Lot/Wafer/Sample ID')
    process_audit_status = models.CharField(max_length=20, blank=True, null=True, db_comment='工序审核状态')

    class Meta:
        managed = False
        db_table = 'sample'
        db_table_comment = '样点列表'
