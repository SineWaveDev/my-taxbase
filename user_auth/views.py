import json

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from knox.models import AuthToken
from .serializers import LoginSerializer, CustomerSerializer
from django.contrib.auth import authenticate
from .services import itd_login, send_sms
from .models import Customer
import pyotp
import base64
from my_taxbase_service.settings import SMS_AUTH_KEY, SMS_TEMPLATE_ID, SMS_SENDER_ID, SMS_TEMPLATE_ID_2
import requests

# Register API


class RegisterAPI(generics.GenericAPIView):
    serializer_class = CustomerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        return Response({
            "customer": CustomerSerializer(customer, context=self.get_serializer_context()).data,
            # "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        try:
            response = authenticate(
                request, username=None, password=request.data['password'])
            if response:
                url = 'http://crm.sinewave.co.in/sinewavelicense/Prod_Usage_Info.aspx'
                params = {
                    'C': request.data['ca_cust_id'],
                    'P': '10055',
                    'V': '',
                    'H': '',
                    'I': '',
                    'L': '',
                    'B': '',
                    'VD': ''
                }
                response_logging = requests.get(url, params=params)
                print(response_logging)
                return Response({"status": True, "message": "User authenticated successfully",
                                 "data": CustomerSerializer(response).data}, status=200)
            return Response({"status": False, "message": "Invalid Credentials"}, status=200)
        except ObjectDoesNotExist as e:
            print(e)
            return Response({"status": False, "message": "User Does Not Exist"}, status=200)


@api_view(['POST'])
def get_user_status(request):
    customer = Customer.objects.filter(
        ca_cust_id=request.data['ca_cust_id'], mobile=request.data['mobile']).first()
    if customer:
        if customer.password:
            response = {
                "status": True,
                "is_verified": True
            }
        else:
            response = {
                "status": True,
                "is_verified": False
            }
    else:
        response = {
            "status": False,
            "message": "Customer ID and Mobile do not match",
            "is_verified": False
        }
        return Response(response, status=200)
    return Response(response, status=200)


@api_view(['POST'])
def set_password(request):
    customer = Customer.objects.filter(
        ca_cust_id=request.data['ca_cust_id'], mobile=request.data['mobile']).first()
    if customer:
        if customer.password:
            response = {
                "status": False,
                "message": "Password was already set. Please use forgot password if you wish to set a new password."
            }
        else:
            customer.password = request.data['password']
            customer.save()
            customer.refresh_from_db()
            response = {
                "status": True,
                "message": "Password setup successfully",
                "data": CustomerSerializer(customer).data
            }
    else:
        response = {
            "status": False,
            "message": "Username and Mobile do not match",
            "is_verified": False
        }
        return Response(response, status=200)
    return Response(response, status=200)


@api_view(['GET'])
def get_otp(request):
    data = request.query_params.dict()
    mobile = data['mobile']
    key = base64.b32encode(mobile.encode())
    otp = pyotp.TOTP(key, digits=6, interval=180)
    otp_str = otp.now()
    if data.get('template_id'):
        template_id = data['template_id']
        sms_data = {"otp": otp_str}
    else:
        template_id = SMS_TEMPLATE_ID
        sms_data = {"otp": otp_str, "appname": "MyTaxbase"}

    print(otp_str)
    send_sms("91" + mobile, sms_data, template_id)
    return Response({"status": True,
                     "message": "An SMS was sent to your registered mobile number. Please enter the one-time password "
                                "it contains."})


@api_view(['GET'])
def get_otp_2(request):
    data = request.query_params.dict()
    mobile = data['mobile']
    key = base64.b32encode(mobile.encode())
    otp = pyotp.TOTP(key, digits=6, interval=180)
    otp_str = otp.now()
    if data.get('template_id'):
        template_id = data['template_id']
        sms_data = {"otp": otp_str}
    else:
        template_id = SMS_TEMPLATE_ID_2
        sms_data = {"otp": otp_str, "appname": "MIS Forget password"}

    print(otp_str)
    send_sms("91" + mobile, sms_data, template_id)
    return Response({"status": True,
                     "message": "An SMS was sent to your registered mobile number. Please enter the one-time password "
                                "it contains."})



@api_view(['GET'])
def get_otp_3(request):
    data = request.query_params.dict()
    mobile = data['mobile']
    key = base64.b32encode(mobile.encode())
    otp = pyotp.TOTP(key, digits=6, interval=180)
    otp_str = otp.now()
    if data.get('template_id'):
        template_id = data['template_id']
        sms_data = {"otp": otp_str}
    else:
        template_id = SMS_TEMPLATE_ID
        sms_data = {"otp": otp_str, "appname": "DSC"}

    print(otp_str)
    send_sms("91" + mobile, sms_data, template_id)
    return Response({"status": True,
                     "message": "An SMS was sent to your registered mobile number. Please enter the one-time password "
                                "it contains."})



@api_view(['GET'])
def verify_otp(request):
    data = request.query_params.dict()
    mobile = data['mobile']
    otp_str = data['otp']
    key = base64.b32encode(mobile.encode())
    otp = pyotp.TOTP(key, digits=6, interval=180)
    if otp.verify(otp_str):
        set_pass_key = base64.b32encode((mobile + otp_str).encode())
        set_pass_token = pyotp.TOTP(set_pass_key, digits=6, interval=180).now()
        return Response({"status": True, "message": "Verification successful", "data": {"pass_token": set_pass_token}})
    else:
        return Response({"status": False,
                         "message": "Incorrect OTP. This might be expired please generate a new one and try again"})


@api_view(['POST'])
def set_forgot_password(request):
    mobile = request.data['mobile']
    set_pass_token = request.data['pass_token']
    password = request.data['password']
    otp_str = request.data['otp']
    set_pass_key = base64.b32encode((str(mobile) + otp_str).encode())
    set_pass_otp = pyotp.TOTP(set_pass_key, digits=6, interval=180)
    if set_pass_otp.verify(set_pass_token):
        customer = Customer.objects.filter(
            mobile=request.data['mobile']).first()
        customer.password = password
        customer.save()
        return Response({"status": True, "message": "Password reset complete"})
    else:
        return Response({"status": False, "message": "Password reset session has expired. Please try again."})


@api_view(['GET'])
def get_customer(request, ca_cust_id):
    try:
        customers = Customer.objects.filter(ca_cust_id=ca_cust_id)

        if customers.exists():
            mobile_numbers = [customer.mobile for customer in customers]
            return Response({"mobile_numbers": mobile_numbers})
        else:
            return Response({"message": "Customers not found for the given ca_cust_id"}, status=404)

    except Customer.DoesNotExist:
        return Response({"message": "Error occurred while retrieving customer information"}, status=500)


@api_view(['POST'])
def add_customer_data(request, ca_cust_id):
    try:
        customers = Customer.objects.filter(ca_cust_id=ca_cust_id)
        if customers.exists():
            customer = customers.first()
        else:
            return Response({"message": "Customer not found"}, status=404)

        if request.method == 'POST':
            serializer = CustomerSerializer(
                customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        else:
            return Response({"message": "Invalid request method"}, status=400)
    except Customer.DoesNotExist:
        return Response({"message": "Customer not found"}, status=404)


@api_view(['DELETE'])
def delete_mobile_number(request, ca_cust_id):
    try:
        # Assuming you pass mobile_number in the request data
        mobile_number_to_delete = request.data.get('mobile_number')

        if not mobile_number_to_delete:
            return Response({"message": "Mobile number not provided in request data"}, status=400)

        customer = Customer.objects.filter(
            ca_cust_id=ca_cust_id, mobile=mobile_number_to_delete).first()

        if customer:
            customer.delete()
            return Response({"message": f"Customer with mobile number {mobile_number_to_delete} deleted successfully"})
        else:
            return Response({"message": f"No customer found with mobile number {mobile_number_to_delete}"}, status=404)

    except Exception as e:
        return Response({"message": "Error occurred while deleting customer"}, status=500)
