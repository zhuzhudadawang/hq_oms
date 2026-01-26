from django.apps import AppConfig


class SyncConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.sync"

    def ready(self):
        """Django 启动时自动启动定时任务"""
        import os
        import sys

        # 跳过 migrate、collectstatic 等管理命令
        if len(sys.argv) > 1 and sys.argv[1] in ['migrate', 'collectstatic', 'makemigrations', 'shell', 'inspectdb', 'check']:
            return

        # 避免开发模式下重复启动（runserver 会启动两次）
        if os.environ.get('RUN_MAIN') == 'true' or 'gunicorn' in sys.modules:
            from apps.sync.tasks import start_scheduler
            start_scheduler()
