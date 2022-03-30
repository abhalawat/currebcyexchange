from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from service_objects.services import Service

from .models import INRTransaction, CryptoLedger


class DepositService(Service):
    username = serializers.CharField(max_length=30)
    deposit = serializers.FloatField()

    def process(self):
        amount = self.data['deposit']
        user = self.data['username']

        qs = User.objects.select_for_update().filter(username=user)[0].profile
        qs.balance = qs.balance + amount
        qs.save()
        transaction1 = INRTransaction(user=user, deposit=amount, balance=qs.balance,
                                      dateTime=timezone.now())
        transaction1.save()


class WithdrawService(Service):
    username = serializers.CharField(max_length=30)
    withdraw = serializers.FloatField()

    def process(self):
        amount = self.data['withdraw']
        user = self.data['username']

        qs = User.objects.select_for_update().filter(username=user)[0].profile
        if qs.balance >= amount:
            qs.balance = qs.balance - amount
            qs.save()
            transaction1 = INRTransaction(user=user, withdraw=amount, balance=qs.balance,
                                          dateTime=timezone.now())
            transaction1.save()
        else:
            raise serializers.ValidationError("amount is greater than balance")


class CryptoDepositService(Service):
    username = serializers.CharField(max_length=30)
    toAdd = serializers.CharField(max_length=30)
    tokenId = serializers.IntegerField()
    quantity = serializers.FloatField()

    def process(self):
        username = self.data['username']
        to_add = self.data['toAdd']
        token_id = self.data['tokenId']
        quantity = self.data['quantity']

        crypto = CryptoLedger(user=username, tokenId=token_id, toAdd=to_add, quantity=quantity)
        crypto.save()


# class TransferService(Service):
#     username = serializers.CharField(max_length=30)
#     toAdd = serializers.CharField(max_length=30)
#     amount = serializers.IntegerField()
#
#     def process(self):
#         username = self.data['username']
#         to_add = self.data['toAdd']
#         amount = self.data['amount']
#
#         transfer = TransferLedger(user=username, amount=amount, toAdd=to_add)
#         transfer.save()
