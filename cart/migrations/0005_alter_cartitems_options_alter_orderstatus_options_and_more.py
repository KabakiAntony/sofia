# Generated by Django 4.1 on 2022-10-28 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_orderstatus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitems',
            options={'verbose_name_plural': 'Cart Items'},
        ),
        migrations.AlterModelOptions(
            name='orderstatus',
            options={'verbose_name_plural': 'Order Status'},
        ),
        migrations.AlterModelOptions(
            name='shippinginformation',
            options={'verbose_name_plural': 'Shipping Information'},
        ),
    ]