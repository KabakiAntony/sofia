from django.db import models
from django.conf import settings


class Region(models.Model):
    region = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.region


class Area(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    area = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.area


class Customer(models.Model):
    """ this holds customer information """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')

    @property
    def get_first_name(self):
        return self.user.first_name

    @property
    def get_last_name(self):
        return self.user.last_name

    @property
    def get_email(self):
        return self.user.email

    def __str__(self):
        return " ".join([self.get_first_name, self.get_last_name])

    class Meta:
        verbose_name_plural = "Customers"


class Address(models.Model):
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, verbose_name="Region")
    area = models.ForeignKey(
        Area, on_delete=models.SET_NULL, null=True, verbose_name="Area")
    street_lane_other = models.CharField(
        max_length=200, blank=True, verbose_name="Street / Lane / Other")
    apartment_suite_building = models.CharField(
        max_length=200, blank=True, verbose_name="Apartment / Suite / Building")
    mobile_no = models.CharField(max_length=13, blank=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='Customer'
    )
    is_default = models.BooleanField(
        default=False, verbose_name="Default Shipping Address")

    def __str__(self):
        return f"{self.customer}'s Address"

    @property
    def get_formatted_address(self):
        parts = [
            self.street_lane_other,
            self.apartment_suite_building,
            f"{self.area}, {self.region}",
        ]

        return ", ".join(part for part in parts if part)

    class Meta:
        verbose_name_plural = "Shipping Addresses"


class ShippingCosts(models.Model):
    area = models.ForeignKey(
        Area, on_delete=models.SET_NULL, null=True, verbose_name="Area")
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"The cost of shipping to {self.area} is {self.cost}"

    class Meta:
        verbose_name_plural = "Shipping Costs"
