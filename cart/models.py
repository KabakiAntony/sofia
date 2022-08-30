from django.db import models
from accounts.models import Customer
from products.models import Product


class Cart(models.Model):
    """ and order is just a cart """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=150)

    def __str__(self):
        return self.customer.email

    @property
    def get_cart_total(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.get_total for item in cartitems])
        return total

    @property
    def get_cart_items(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.quantity for item in cartitems])
        return total


class CartItems(models.Model):
    """ these are the items on the cart """
    cart =  models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    product =  models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingInformation(models.Model):
    """ this will hold a customer shipping information"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    cart =  models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    mobile_no = models.CharField(max_length=13, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

