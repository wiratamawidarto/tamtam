from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import mylinebot
# Create your models here.


class Manager(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    line_id = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True, default='no')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Manager"


class AlertNotification(models.Model):
    alert_id = models.ForeignKey('db_api.Yolo', on_delete=models.CASCADE, null=True)
    line_user = models.ForeignKey('employee.employee', on_delete=models.CASCADE, null=True)
    received = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=timezone.now)
    task_id = models.CharField(max_length=500, null=True, blank=True, default='')
    memo = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(editable=True, null=True, blank=True)

    def __str__(self):
        return self.line_user.name

    class Meta:
        db_table = "AlertNotification"


class AlertImageNotification(models.Model):
    alert_id = models.ForeignKey('db_api.Yolo_Files', on_delete=models.CASCADE, null=True)
    line_user = models.ForeignKey('employee.employee', on_delete=models.CASCADE, null=True)
    received = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=True, default=timezone.now)
    task_id = models.CharField(max_length=500, null=True, blank=True, default='')
    memo = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(editable=True, null=True, blank=True)

    def __str__(self):
        return self.line_user.name

    class Meta:
        db_table = "AlertImageNotification"


@receiver(post_save, sender=AlertNotification)
def push_alert_notification(sender, instance, created, **kwargs):
    if created and instance.received == False:
        task_id = mylinebot.alert.append_task_queue(instance)
        instance.task_id = task_id
        instance.save()

    elif not created and instance.received == True:
        mylinebot.alert.remove_task_from_queue(instance.task_id)


@receiver(post_save, sender=AlertImageNotification)
def push_alert_img_notification(sender, instance, created, **kwargs):
    if created and instance.received == False:
        task_id = mylinebot.alert.append_imgtask_queue(instance)
        instance.task_id = task_id
        instance.save()
