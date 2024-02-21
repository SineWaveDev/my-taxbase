from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Customer(AbstractBaseUser):
    ca_cust_id = models.CharField(max_length=20, db_column="ca_cust_id", verbose_name=u"CA Customer ID")
    password = models.CharField(max_length=128, null=True, default=None, blank=True)
    mobile = models.CharField(max_length=20, unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password):
        if self.password != "" or self.password is not None:
            self.password = make_password(raw_password)

    EMAIL_FIELD = "mobile"
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ["mobile"]
