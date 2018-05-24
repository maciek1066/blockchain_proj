from django.shortcuts import render
from django.views import View
from address_info.forms import AddressForm


class AddressInfoView(View):
    def get(self, request):
        form = AddressForm()
        ctx = {
            'form': form,
        }
        return render(
            request,
            template_name="main.html",
            context=ctx
        )
