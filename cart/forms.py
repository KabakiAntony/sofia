from django import forms
from customers.models import Area, Address

class CheckoutForm(forms.ModelForm):
    firstname = forms.CharField(
        label="First name",
        max_length=150,
        widget=forms.TextInput(attrs={'required':True}),
        required=True
        )
    lastname = forms.CharField(
        label="Last name",
        max_length=150,
        widget=forms.TextInput(attrs={'required':True}),
        required=True
        )
    email = forms.EmailField(
        label="Email",
        max_length=255,
        widget=forms.EmailInput(attrs={'required':True}),
        required=True
    )
    mobile_no = forms.CharField(
        label="Mobile No",
        max_length=10,
        widget=forms.TextInput(attrs={'required':True}),
        required=True
        )
    
    street_lane_other = forms.CharField(
        label="Street / Lane / Other ",
        max_length=100,
        widget=forms.TextInput,
        required=False
    )
    apartment_suite_building = forms.CharField(
        label="Apartment / Suite / Building",
        max_length=100,
        widget=forms.TextInput,
        required=False
    )

    class Meta:
        model = Address
        fields = ['region', 'area']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['area'].queryset = Area.objects.filter(region=region_id).order_by('area')
            except(ValueError, TypeError):
                pass
        elif self.instance.id:
            self.fields['area'].queryset = self.instance.region.area_set.order_by('area')