from django import forms
from .models import Address, Area


class AddressForm(forms.ModelForm):
    mobile_no = forms.CharField(
        label="Mobile No",
        max_length=10,
        widget=forms.TextInput(),
        required=True
        )

    class Meta:
        model = Address
        fields = ['mobile_no', 'region', 'area', 'street_lane_other', 'apartment_suite_building']


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


    
