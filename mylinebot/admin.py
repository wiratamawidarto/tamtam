from django.contrib import admin
from .models import Manager, AlertNotification, AlertImageNotification

# Register your models here.

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'line_id', 'state')


class AlertNotificationAdmin(admin.ModelAdmin):
    list_display = ('alert_id', 'line_user', 'received', 'created_at', 'timestamp')


class AlertImageNotificationAdmin(admin.ModelAdmin):
    list_display = ('alert_id', 'line_user', 'received', 'created_at', 'timestamp')


admin.site.register(Manager, ManagerAdmin)
admin.site.register(AlertNotification, AlertNotificationAdmin)
admin.site.register(AlertImageNotification, AlertImageNotificationAdmin)
