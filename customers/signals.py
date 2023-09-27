from django.conf import settings 
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()