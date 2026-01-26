"""
手动测试同步脚本
运行方式: python apps/sync/run_sync.py
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HQ_OMS.settings')
django.setup()

# 配置日志输出到控制台
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    # 测试机台表同步
    # from apps.sync.tasks import sync_machine
    # sync_machine()

    # 测试机台耗时记录同步
    # from apps.sync.tasks import sync_machine_usage
    # sync_machine_usage()
    
    # 测试工序表同步
    # from apps.sync.tasks import sync_process
    # sync_process()
    
    # 测试订单表同步
    from apps.sync.tasks import sync_order
    sync_order()
    
    # 测试样点表同步
    from apps.sync.tasks import sync_sample
    sync_sample()
