from django.db import models
from customers.models import Customer
from products.models import Product_Entry
from django.http import HttpResponse


class Cart(models.Model):
    """ and order is just a cart """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.UUIDField(null=True,editable=False)

    def __str__(self):
        return self.customer.email +"_cart_id_"+str(self.id)

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
    
    @property
    def get_shipping_amount(self):
        shipping_amount = 350
        return shipping_amount

    @property
    def get_pickup_amount(self):
        pickup_amount = 0
        return pickup_amount
    
    @property
    def get_shipping_n_cart_total(self):
        return  self.get_cart_total + self.get_shipping_amount

    @property
    def get_pickup_n_cart_total(self):
        return self.get_cart_total + self.get_pickup_amount


class CartItems(models.Model):
    """ these are the items on the cart """
    cart =  models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    product =  models.ForeignKey(Product_Entry, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    class Meta:
        verbose_name_plural ="Cart Items"


class OrderStatus(models.Model):
    """ this will hold order status"""
    
    transaction_id = models.CharField(max_length=150)
    status = models.CharField(max_length=50)
    result_code = models.CharField(max_length=2)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "Order Status"

class ReceivedOrder(models.Model):
    class Meta:
        verbose_name_plural = "Received Orders"
        # app_label = "ReceivedOrder"

    def show_orders(request):
        return HttpResponse("This is a custom view")