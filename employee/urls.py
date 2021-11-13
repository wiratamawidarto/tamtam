from django.urls import path
from .views import profile, update_profile

urlpatterns = [
    path('profile/', profile, name='my_profile'),
    path('profile/update', update_profile, name='my_profile_update'),
]