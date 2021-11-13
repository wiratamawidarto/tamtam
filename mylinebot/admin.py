from django.contrib import admin
from .models import Manager

# Register your models here.

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'line_id', 'state')


admin.site.register(Manager, ManagerAdmin)