# custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_default_address(addresses):
    return addresses.filter(is_default=True).first()
