from .views import RegisterAPI, LoginAPI, get_user_status, set_password, get_otp, verify_otp, set_forgot_password, get_otp_2
from django.urls import path

urlpatterns = [
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('user_status', get_user_status, name='user_status'),
    path('set_password', set_password, name='set_password'),
    path('get_otp', get_otp, name='get_otp'),
    path('get_otp_2', get_otp_2, name='get_otp_2'),
    path('verify_otp', verify_otp, name='verify_otp'),
    path('set_forgot_password', set_forgot_password, name='set_forgot_password')
]
