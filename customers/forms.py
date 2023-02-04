from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    mobile_no = forms.CharField(
        label="Mobile No.",
        max_length=10,
        widget=forms.TextInput(),
        required=True)

    class Meta:
        model = Address
        fields = ['mobile_no','region', 'street_lane_other', 'apartment_suite_building']
