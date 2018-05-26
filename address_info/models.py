from django.contrib.postgres.fields import JSONField
from django.db import models


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=256)
    tx_inputs = JSONField()
    tx_outs = JSONField()
    timestamp = models.IntegerField(null=True)


class Address(models.Model):
    address = models.CharField(max_length=35)
    hash160 = models.CharField(max_length=54)
    no_transactions = models.IntegerField()
    received = models.BigIntegerField()
    sent = models.BigIntegerField()
    balance = models.BigIntegerField()
    transactions = models.ManyToManyField(Transaction)
