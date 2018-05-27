from django.contrib.postgres.fields import JSONField
from django.db import models


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=256)
    tx_inputs = JSONField()
    tx_outs = JSONField()
    inp_sum = models.BigIntegerField()
    out_sum = models.BigIntegerField()
    time = models.DateTimeField(null=True)

    def inp_sum_bit(self):
        return self.inp_sum / 100000000

    def out_sum_bit(self):
        return self.out_sum / 100000000


class Address(models.Model):
    address = models.CharField(max_length=35)
    hash160 = models.CharField(max_length=54)
    no_transactions = models.IntegerField()
    received = models.BigIntegerField()
    sent = models.BigIntegerField()
    balance = models.BigIntegerField()
    transactions = models.ManyToManyField(Transaction)

    def received_bit(self):
        return self.received / 100000000

    def sent_bit(self):
        return self.sent / 100000000

    def balance_bit(self):
        return self.balance / 100000000
