# from django.conf.urls import url
# from .views import FileView
# urlpatterns = [
#     url(r'^upload/$', FileView.as_view(), name='file-upload'),
# ]

from django.conf.urls import url
from db_api.views import YoloView, AlertYoloView
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'/yolo', YoloView)
# router.register(r'alert/yolo', AlertYoloView)


# urlpatterns = [
#     url(r'^yolo/$', YoloView, name='yoloview'),
#     url(r'^alert/yolo/$', AlertYoloView, name='alertyolo'),
# ]