from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from address_info.models import Address, Transaction
from address_info.forms import AddressForm
from time import strftime
from datetime import datetime
import requests
from django.utils import timezone
from django.db.models import Count, Sum
import qrcode


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
                addr = Address.objects.get(address=address)
                txs = addr.transactions.all()
                ctx = {
                    "addr": addr,
                    "txs": txs,
                }
                if request.POST.get('date') == 'date_filter':
                    since = request.POST.get('since')
                    to = request.POST.get('to')
                    txs = addr.transactions.filter(time__range=(since, to))
                    txs_count = txs.aggregate(Count('transaction_id'))
                    tx_inp_sum = txs.aggregate(Sum('inp_sum'))
                    tx_balance = txs.aggregate(balance=(Sum('inp_sum')) - (Sum('out_sum')))
                    if isinstance(tx_balance["balance"], int) and tx_balance["balance"] != 0:
                        tx_balance["balance"] = tx_balance["balance"]/100000000
                    if isinstance(tx_inp_sum["inp_sum__sum"], int) and tx_inp_sum["inp_sum__sum"] != 0:
                        tx_inp_sum["inp_sum__sum"] = tx_inp_sum["inp_sum__sum"]/100000000
                    trx_filter = True

                    ctx = {
                        "trx_filter": trx_filter,
                        "addr": addr,
                        "txs": txs,
                        "txs_count": txs_count,
                        "tx_inp_sum": tx_inp_sum,
                        "tx_balance": tx_balance,
                    }
                return render(
                    request,
                    "addr_result.html",
                    context=ctx
                )
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

                # creating QR code for address
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=3,
                    border=4,
                )
                data_img = address
                qr.add_data(data_img)
                qr.make(fit=True)
                img = qr.make_image()
                img.save("media/{}.jpg".format(address))

                # transactions for given address
                for i in range(len(data["txs"])):
                    #  counting input/output sums
                    inp_sum = 0
                    out_sum = 0
                    for inp in data["txs"][i]["inputs"]:
                        inp_sum += (inp["prev_out"]["value"])
                    for out in data["txs"][i]["out"]:
                        out_sum += (out["value"])

                    new_trx = Transaction.objects.create(
                        transaction_id=data["txs"][i]["hash"],
                        tx_inputs=data["txs"][i]["inputs"],
                        tx_outs=data["txs"][i]["out"],
                        inp_sum=inp_sum,
                        out_sum=out_sum,
                        time=timezone.make_aware(
                            datetime.fromtimestamp(data["txs"][i]["time"])
                        )
                    )
                    addr = Address.objects.get(address=data["address"])
                    addr.transactions.add(new_trx)
                    addr.save()
                txs = addr.transactions.all()
                ctx = {
                    "addr": addr,
                    "txs": txs,
                }
                if request.POST.get('date') == 'date_filter':
                    since = request.POST.get('since')
                    to = request.POST.get('to')
                    txs = addr.transactions.filter(time__range=(since, to))
                    txs_count = txs.aggregate(Count('transaction_id'))
                    tx_inp_sum = txs.aggregate(Sum('inp_sum'))
                    tx_inp_sum["inp_sum__sum"] = tx_inp_sum["inp_sum__sum"]/100000000
                    tx_balance = txs.aggregate(balance=(Sum('inp_sum')) - (Sum('out_sum')))
                    if isinstance(tx_balance["balance"], int) and tx_balance["balance"] != 0:
                        tx_balance["balance"] = tx_balance["balance"]/100000000
                    if isinstance(tx_inp_sum["inp_sum__sum"], int) and tx_inp_sum["inp_sum__sum"] != 0:
                        tx_inp_sum["inp_sum__sum"] = tx_inp_sum["inp_sum__sum"]/100000000
                    trx_filter = True
                    ctx = {
                        "trx_filter": trx_filter,
                        "addr": addr,
                        "txs": txs,
                        "txs_count": txs_count,
                        "tx_inp_sum": tx_inp_sum,
                        "tx_balance": tx_balance,
                    }
                return render(
                    request,
                    "addr_result.html",
                    context=ctx
                )



