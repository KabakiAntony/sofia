from django.db import models
from customers.models import Customer
from products.models import Product_Entry


class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.user.email + "_cart_id_"+str(self.id)

    @property
    def cart_total(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.get_total for item in cartitems])
        return total

    @property
    def total_items_on_cart(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    product_entry = models.ForeignKey(
        Product_Entry, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_entry.title

    @property
    def get_total(self):
        total = self.product_entry.price * self.quantity
        return total

    class Meta:
        verbose_name_plural = "Cart Items"
