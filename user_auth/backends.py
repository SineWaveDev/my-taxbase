from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from .models import Customer


class CustomerBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        mobile = request.data['mobile']
        ca_cust_id = request.data['ca_cust_id']
        try:
            customer = Customer.objects.get(ca_cust_id=ca_cust_id, mobile=mobile)
        except ObjectDoesNotExist as e:
            raise e
        if customer:
            if customer.password:
                pwd_valid = password == customer.password
                if pwd_valid:
                    return customer
                else:
                    return None
            else:
                return None
        else:
            return None
