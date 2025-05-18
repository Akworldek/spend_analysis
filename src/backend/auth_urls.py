from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import register_user, logout_user

urlpatterns = [
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
]