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
