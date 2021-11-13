from django.contrib import admin
from employee.models import employee
from employee.models import Company


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'gongHao', 'company', 'lineid')

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','name2')


admin.site.register(employee, EmployeeAdmin)
admin.site.register(Company, CompanyAdmin)

# Register your models here.
