from .views import RegisterAPI, LoginAPI, delete_mobile_number, add_customer_data, get_user_status, set_password, get_otp, verify_otp, set_forgot_password, get_otp_2, get_customer, get_otp_3
from django.urls import path

urlpatterns = [
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('get_otp', get_otp, name='get_otp'),
    path('get_otp_2', get_otp_2, name='get_otp_2'),
    path('get_otp_3', get_otp_3, name='get_otp_3'),
    path('verify_otp', verify_otp, name='verify_otp'),
    path('set_password', set_password, name='set_password'),
    path('set_forgot_password', set_forgot_password, name='set_forgot_password'),
    path('user_status', get_user_status, name='user_status'),
    path('api/customer/<str:ca_cust_id>/', get_customer, name='get_customer'),
    path('api/customer/<str:ca_cust_id>/add-data/',
         add_customer_data, name='add_customer_data'),
    path('api/customer/<str:ca_cust_id>/delete-mobile/',
         delete_mobile_number, name='delete_mobile_number'),
]
