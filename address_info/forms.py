from django.forms import ModelForm
from address_info.models import Address


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['address']