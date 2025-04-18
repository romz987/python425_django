from django.urls import path 

from users.apps import UsersConfig 
from users.views import *

app_name = UsersConfig.name 


urlpatterns = [
    path('', user_login_view, name='user_login'),
    path('logout/', user_logout_view, name='user_logout'),
    path('register/', user_register_view, name='user_register'),
    path('profile/', user_profile_view, name='user_profile'),
    path('update/', user_update_view, name='user_update'),
    path('change_password', user_change_password_view, name='user_change_password')
]

