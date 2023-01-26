from django.db import models
from django.conf import settings


class Customer(models.Model):
    """ this holds customer information """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=13, blank=True)

    def __str__(self):
        return self.user.email

    @property
    def get_first_name(self): 
        return self.user.first_name

    @property
    def get_last_name(self):
        return self.user.last_name

    class Meta:
        verbose_name_plural = "Customers"


class Region(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    street_lane_other = models.CharField(max_length=200, blank=True)
    apartment_suite_building = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.customer
    

    class Meta:
        verbose_name_plural = "Shipping Address"


