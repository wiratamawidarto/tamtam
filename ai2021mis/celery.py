import os
from celery import Celery
from django.conf import settings

# Celery
# 設置環境變量 DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai2021mis.settings')
# 創建實例 Create celery
app = Celery('ai2021mis')
app.config_from_object('django.conf:settings')
# 查找在 INSTALLED_APPS 設置的異步任務
app.autodiscover_tasks()


# 一個測試任務
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
