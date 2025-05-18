from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
from .views import register_user, logout_user

urlpatterns = [
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

]