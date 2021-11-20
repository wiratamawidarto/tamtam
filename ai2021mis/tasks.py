# myproject/tasks.py
# 專屬於myproject專案的任務
from celery import Celery
app = Celery('ai2021mis')

@app.task(name='push-message')
def test():
    pass
