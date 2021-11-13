from django.contrib import admin
from db_api.models import Yolo, Yolo_Files, Alert_Data, yolo_trial,Picture_Files
# Register your models here.

class YoloAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'timestamp')


class Yolo_FilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')

class Alert_Data_Admin(admin.ModelAdmin):
    list_display= ('id','body')

class yolotrial_Admin(admin.ModelAdmin):
    list_display=('id','title')

class Picture_Files_Admin(admin.ModelAdmin):
    list_display = ('identifier', 'picture', 'memo')



admin.site.register(Alert_Data, Alert_Data_Admin)
admin.site.register(Yolo, YoloAdmin)
admin.site.register(Yolo_Files, Yolo_FilesAdmin)

admin.site.register(yolo_trial,yolotrial_Admin)
admin.site.register(Picture_Files, Picture_Files_Admin)