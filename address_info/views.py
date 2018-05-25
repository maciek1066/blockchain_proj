from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from address_info.models import Address, Transaction
from address_info.forms import AddressForm
import requests


class AddressInfoView(View):
    def get(self, request):
        form = AddressForm()
        ctx = {
            'form': form,
        }
        return render(
            request,
            template_name='main.html',
            context=ctx
        )

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            if Address.objects.filter(
                    address__contains=address).exists():
                return HttpResponse("Nice")
            else:
                response = requests.get(
                    "https://blockchain.info/rawaddr/{}".format(address))
                data = response.json()
                txs_data = data["txs"]
                return HttpResponse("{}".format(transactions))




