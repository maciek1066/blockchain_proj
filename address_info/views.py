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
                return HttpResponse("Address already exists in db")
            else:
                response = requests.get(
                    "https://blockchain.info/rawaddr/{}".format(address))
                data = response.json()
                #  creating account
                address = data["address"]
                hash160 = data["hash160"]
                no_transactions = data["n_tx"]
                received = data["total_received"]
                sent = data["total_sent"]
                balance = data["final_balance"]
                Address.objects.create(
                    address=address,
                    hash160=hash160,
                    no_transactions=no_transactions,
                    received=received,
                    sent=sent,
                    balance=balance,
                )
                # transactions many to many relation
                for i in range(len(data["txs"])):
                    new_trx = Transaction.objects.create(
                        transaction_id=data["txs"][i]["hash"],
                        tx_inputs=data["txs"][i]["inputs"],
                        tx_outs=data["txs"][i]["out"],
                        timestamp=data["txs"][i]["time"]
                    )
                    addr = Address.objects.get(address=data["address"])
                    addr.transactions.add(new_trx)
                    addr.save()
                return HttpResponse("ziała")




