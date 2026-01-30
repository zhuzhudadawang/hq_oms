# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ManagementFinance(models.Model):
    id = models.BigAutoField(primary_key=True, db_comment='主键ID')
    report_month = models.DateField(unique=True, db_comment='报告月份')
    operating_revenue = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='营业收入')
    operating_cost = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='营业成本')
    gross_profit = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='毛利额')
    gross_margin = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, db_comment='毛利率')
    period_expenses = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='期间费用')
    non_operating_income = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='营业外收入')
    non_operating_expenses = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='营业外支出')
    net_profit = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='净利润')
    created_at = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    updated_at = models.DateTimeField(blank=True, null=True, db_comment='更新时间')

    class Meta:
        managed = False
        db_table = 'management_finance'
        db_table_comment = '管理层财务概况表'


class FounderShareholderFinance(models.Model):
    id = models.BigAutoField(primary_key=True, db_comment='主键ID')
    report_month = models.DateField(unique=True, db_comment='报告月份')
    operating_revenue = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='营业收入')
    operating_cost = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='营业成本')
    gross_profit = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='毛利额')
    gross_margin = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, db_comment='毛利率')
    period_expenses = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='期间费用')
    non_operating_income = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='营业外收入')
    non_operating_expenses = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='营业外支出')
    net_profit = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='净利润')
    total_assets = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='资产总额')
    total_liabilities = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='负债总额')
    shareholders_equity = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='股东权益')
    current_funds = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='活期资金')
    financial_products = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='理财资金')
    unused_loan_limit = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='未使用贷款额度')
    created_at = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    updated_at = models.DateTimeField(blank=True, null=True, db_comment='更新时间')

    class Meta:
        managed = False
        db_table = 'founder_shareholder_finance'
        db_table_comment = '创始股东财务概况表'


class AssetAnalysis(models.Model):
    id = models.BigAutoField(primary_key=True, db_comment='主键ID')
    report_month = models.DateField(unique=True, db_comment='报告月份')
    total_assets = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='资产总额')
    total_liabilities = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='负债总额')
    shareholders_equity = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='股东权益')
    asset_liability_ratio = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, db_comment='资产负债率')
    cash_to_asset_ratio = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, db_comment='货币占总资产比率')
    funds_wealth_management = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='资金+理财')
    inventory = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='存货')
    prepaid_accounts = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='预付账款')
    notes_receivable_accounts = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='应收票据及账款')
    other_receivables = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='其他应收款')
    non_current_assets = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='非流动资产')
    input_tax = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='进项税')
    created_at = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    updated_at = models.DateTimeField(blank=True, null=True, db_comment='更新时间')

    class Meta:
        managed = False
        db_table = 'asset_analysis'
        db_table_comment = '创始股东资产分析表'


class TransactionDetail(models.Model):
    id = models.BigAutoField(primary_key=True, db_comment='主键ID')
    report_month = models.DateField(db_comment='报告月份')
    data_view_type = models.CharField(max_length=30, db_comment='数据视角类型: management(管理层)、founder_shareholder(创始股东)')
    asset_liability_type = models.CharField(max_length=20, db_comment='资产/负债类型: asset(资产类)、liability(负债类)')
    main_subject = models.CharField(max_length=50, db_comment='科目大类: 负债类-advance_from_customer(预收账款)、accounts_payable(应付账款)、other_payables(其他应付款); 资产类-prepaid_accounts(预付账款)、accounts_receivable(应收账款)、notes_receivable(应收票据)、other_receivables(其他应收款)')
    business_partner = models.CharField(max_length=200, blank=True, null=True, db_comment='往来单位')
    balance_amount = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='余额')
    period_0_1y = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='0-1年账期金额')
    period_1_2y = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='1-2年账期金额')
    period_over_2y = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, db_comment='2年以上账期金额')
    specific_situation = models.TextField(blank=True, null=True, db_comment='具体情况说明')
    created_at = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    updated_at = models.DateTimeField(blank=True, null=True, db_comment='更新时间')

    class Meta:
        managed = False
        db_table = 'transaction_detail'
        db_table_comment = '往来款明细表'

class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=30, db_comment='订单编号')
    customer = models.CharField(max_length=30, blank=True, null=True, db_comment='客户')
    priority = models.CharField(max_length=10, blank=True, null=True, db_comment='优先级')
    order_status = models.CharField(max_length=20, blank=True, null=True, db_comment='订单状态')
    sample_status = models.CharField(max_length=20, blank=True, null=True, db_comment='样品状态')
    process_status = models.CharField(max_length=20, blank=True, null=True, db_comment='工序状态')
    order_category = models.CharField(max_length=20, blank=True, null=True, db_comment='订单类目')
    sample_quantity = models.IntegerField(blank=True, null=True, db_comment='样点数量')
    sender_name = models.CharField(max_length=50, blank=True, null=True, db_comment='寄件人名称')
    sender_phone = models.CharField(max_length=50, blank=True, null=True, db_comment='寄件人电话')
    sample_receiver = models.CharField(max_length=20, blank=True, null=True, db_comment='样点接收人员')
    sample_receipt_image = models.CharField(max_length=255, blank=True, null=True, db_comment='样点接受留图（弃用）')
    order_salesman = models.CharField(max_length=20, blank=True, null=True, db_comment='订单销售')
    sales_contact = models.CharField(max_length=20, blank=True, null=True, db_comment='销售联系方式')
    is_outsource = models.CharField(max_length=10, blank=True, null=True, db_comment='是否委外')
    order_type = models.CharField(max_length=20, blank=True, null=True, db_comment='订单类型')
    customer_id = models.CharField(max_length=20, blank=True, null=True, db_comment='客户编号')
    demo_case = models.CharField(max_length=20, blank=True, null=True, db_comment='demo案件')
    receive_time = models.DateTimeField(blank=True, null=True, db_comment='接收时间')
    requirement_confirm_time = models.DateTimeField(blank=True, null=True, db_comment='需求确认时间')
    validity_start_time = models.DateTimeField(blank=True, null=True, db_comment='时效起算时间')
    closing_date = models.DateTimeField(blank=True, null=True, db_comment='结案日期')
    customer_reconciliation_date = models.DateTimeField(blank=True, null=True, db_comment='客户对账日期')
    invoice_date = models.DateTimeField(blank=True, null=True, db_comment='开票日期')
    handlebook_attachment = models.CharField(max_length=255, blank=True, null=True, db_comment='Handlebook附件')
    review_department = models.CharField(max_length=20, blank=True, null=True, db_comment='审核部门')
    reviewer = models.CharField(max_length=20, blank=True, null=True, db_comment='审核人')
    review_time = models.DateTimeField(blank=True, null=True, db_comment='审核时间')
    review_reason = models.CharField(max_length=255, blank=True, null=True, db_comment='审核原因')
    outsourcing_supplier = models.CharField(max_length=20, blank=True, null=True, db_comment='外包供应商')
    upload_result = models.CharField(max_length=255, blank=True, null=True, db_comment='上传结果')
    customer_order_number = models.CharField(max_length=255, blank=True, null=True, db_comment='客户单号')
    closing_time = models.TimeField(blank=True, null=True, db_comment='结案时间')
    customer_requirement = models.TextField(blank=True, null=True, db_comment='客户需求')
    closer = models.CharField(max_length=50, blank=True, null=True, db_comment='结案人')
    commission_to_report_validity = models.CharField(max_length=20, blank=True, null=True, db_comment='委案到报告时效')
    sample_to_report_validity = models.CharField(max_length=20, blank=True, null=True, db_comment='收样到报告时效')
    case_analysis_project_type = models.CharField(max_length=255, blank=True, null=True, db_comment='案例分析项目类型')
    validity_requirement_hours = models.FloatField(blank=True, null=True, db_comment='时效要求(h)')
    customer_bill_status = models.CharField(max_length=20, blank=True, null=True, db_comment='客户账单状态')
    engineer_bill_status = models.CharField(max_length=20, blank=True, null=True, db_comment='工程师账单状态')
    machine_bill_status = models.CharField(max_length=20, blank=True, null=True, db_comment='机台账单状态')
    order_amount = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True, db_comment='订单金额')
    review_date = models.DateTimeField(blank=True, null=True, db_comment='审核日期')
    create_time = models.DateTimeField(db_comment='创建时间')
    modify_time = models.DateTimeField(db_comment='修改时间')
    sender = models.CharField(max_length=20, blank=True, null=True, db_comment='寄件人')
    sender_email = models.CharField(max_length=50, blank=True, null=True, db_comment='寄件人邮箱')
    requirement_confirm_date = models.DateTimeField(blank=True, null=True, db_comment='需求确认日期')
    test_item = models.CharField(max_length=20, blank=True, null=True, db_comment='检测项')
    is_report_required = models.CharField(max_length=10, blank=True, null=True, db_comment='是否需要报告')
    report_format = models.CharField(max_length=20, blank=True, null=True, db_comment='报告形式')
    sample_processing_method = models.CharField(max_length=20, blank=True, null=True, db_comment='样品处理方法')
    execution_place = models.CharField(max_length=20, blank=True, null=True, db_comment='执行地')
    is_order_successful = models.CharField(max_length=10, blank=True, null=True, db_comment='订单是否一次性成功')
    specimen_quantity = models.IntegerField(blank=True, null=True, db_comment='样品数量')

    class Meta:
        managed = False
        db_table = 'order'

class Orderitem(models.Model):
    id = models.BigAutoField(primary_key=True)
    project = models.CharField(max_length=200, blank=True, null=True, db_comment='项目')
    quantity = models.IntegerField(blank=True, null=True, db_comment='数量')
    unit = models.CharField(max_length=50, blank=True, null=True, db_comment='单位')
    unit_price_before_tax = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True, db_comment='单价（未税）')
    unit_price_after_tax = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True, db_comment='单价（含税）')
    amount_before_tax = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True, db_comment='金额（未税）')
    amount_after_tax = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True, db_comment='金额（含税）')
    billing_quantity = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_comment='计价数量')
    tax_rate = models.CharField(max_length=20, blank=True, null=True, db_comment='税率')
    order_id = models.CharField(max_length=50, blank=True, null=True, db_comment='关联订单')
    customer = models.CharField(max_length=100, blank=True, null=True, db_comment='客户')
    commission_date = models.DateField(blank=True, null=True, db_comment='委案日期')
    commissioner = models.CharField(max_length=100, blank=True, null=True, db_comment='委托人')
    remark = models.TextField(blank=True, null=True, db_comment='备注')
    validity_hours = models.IntegerField(blank=True, null=True, db_comment='时效(h)')
    validity_start_date = models.DateField(blank=True, null=True, db_comment='时效开始日期')
    validity_start_time = models.CharField(max_length=20, blank=True, null=True, db_comment='时效起算时间')

    class Meta:
        managed = False
        db_table = 'orderitem'
        db_table_comment = '订单项目表'