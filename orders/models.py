from django.db import models
from django.urls import reverse
from customers.models import Customer, Address
from products.models import Product_Entry


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="shipping_address")
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_or_pickup = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"This is {self.customer}'s order ID {self.id}"
    
    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})

    @property
    def get_order_total(self):
        return self.order_total

    @property
    def get_shipping_cost(self):
        return self.shipping_cost
    
    @property
    def get_shipping_n_order_total(self):
        return self.get_shipping_cost + self.get_order_total
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_entry =  models.ForeignKey(Product_Entry, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product_entry.title

    @property
    def get_total(self):
        total = self.product_entry.price * self.quantity
        return total
    
    class Meta:
        verbose_name_plural ="Order Items"


class Payment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.UUIDField(null=True, editable=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f'{self.order.customer} status {self.status}'

