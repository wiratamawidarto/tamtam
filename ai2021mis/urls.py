"""ai2021mis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from db_api.views import YoloView, YoloFilesView, PictureFilesView
from .views import LoginPage, LogOutPage

from db_api.models import Yolo
from django.http import HttpResponse
def test(request):
    all_data = Yolo.objects.filter(title = 'test.jpg')
    try:
        result =[]
        for pic in all_data:
            result.append(pic.image)
    except Exception as e:
        result = e
    return HttpResponse(result)


router = DefaultRouter()
router.register('yolo', YoloView)
router.register('yolo-files', YoloFilesView)
router.register('picture-files',PictureFilesView)
# router.register('yolo-alert', AlertYoloView)
# router.register('yolo-post', YoloPostView, basename='yolo-post')

urlpatterns = [
    path('', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^linebot/', include('mylinebot.urls')),
    url(r'^website/', include('website.urls')),
    url(r'^user/', include('employee.urls')),
    # path('accounts/', include('allauth.urls')),
   # path('login/', LoginPage),
    path('login/', LoginPage, name='login'),
    path('logout/', LogOutPage, name='logout'),
    path('test/', test),

] + static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)

