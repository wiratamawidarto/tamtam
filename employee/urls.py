from django.urls import path
from .views import profile, update_profile, update_line_id, user_login_line

urlpatterns = [
    path('profile/', profile, name='my_profile'),
    path('profile/update', update_profile, name='my_profile_update'),
    path('profile/update/update_line_id/', update_line_id,  name='my_line_id_update'),
    path('profile/UserLoginLine/', user_login_line, name='user_login_line'),
]
