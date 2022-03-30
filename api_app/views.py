from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import INRTransaction, CryptoLedger
from .serializers import WalletSerializer, TransactionSerializer, AmountSerializer, \
    WithdrawSerializer, CryptoLedgerSerializer, CryptoSerializer
from .services import DepositService, WithdrawService, CryptoDepositService


class CryptoTransactionViewSet(viewsets.ModelViewSet):
    model = CryptoLedger
    queryset = CryptoLedger.objects.all()
    serializer_class = CryptoSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_balance_view(request, *args, **kwargs):
    try:
        qs = User.objects.filter(username=request.user)[0].profile
        serializer = WalletSerializer(qs)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"Something went wrong. Please try again later."}, status=status.HTTP_404_NOT_FOUND)

# user = models.CharField(max_length=10)
#     balance = models.FloatField(default=0.0)
#     deposit = models.FloatField(default=0.0)
#     deposit_to = models.CharField(max_length=30)
#     deposit_from = models.CharField(max_length=30)
#     withdraw = models.FloatField(default=0.0)
#     withdraw_to = models.CharField(max_length=30)
#     withdraw_from = models.CharField(max_length=30)
#     dateTime = models.DateTimeField(auto_now_add=True, null=True)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def deposit_balance_view(request, *args, **kwargs):
#     with transaction.atomic():
#         serializer = AmountSerializer(data=request.data)
#         # {"amount": 2}
#         if serializer.is_valid(raise_exception=True):
#             DepositService.execute({
#                 'username': request.user,
#                 'deposit': serializer.initial_data['amount']
#             })
#         return Response({"Deposit successful."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_balance_view(request, *args, **kwargs):
    with transaction.atomic():
        try:
            serializer = AmountSerializer(data=request.data)
            # {"amount": 2}
            # {"amount": 2,"deposit_to": 2,"deposit_from": "bank"}
            if serializer.is_valid(raise_exception=True):
                DepositService.execute({
                    'username': request.user,
                    'deposit': serializer.initial_data['amount']
                })
            return Response({"Deposit successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"Deposit unsuccessful."}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw_balance_view(request, *args, **kwargs):
    try:
        with transaction.atomic():
            serializer = WithdrawSerializer(data=request.data)
            # {"amount": 2}
            if serializer.is_valid(raise_exception=True):
                WithdrawService.execute({
                    'username': request.user,
                    'withdraw': serializer.initial_data['amount']
                })
            return Response({"Withdraw successful."}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"Something went wrong. Please try again later."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_balance_view(request, *args, **kwargs):
    try:
        login_user = str(request.user)
        if login_user != 'admin':
            qs = INRTransaction.objects.filter(user=request.user)
            data = []
            for i in qs:
                serializer = TransactionSerializer(i)
                data.append(serializer.data)
            return Response(data, status=200)
        else:
            queryset = INRTransaction.objects.all()
            data = []
            for i in queryset:
                serializer = TransactionSerializer(i)
                data.append(serializer.data)
            return Response(data, status=200)
    except Exception as e:
        print(e)
        return Response({"Something went wrong. Please try again later."}, status=status.HTTP_404_NOT_FOUND)


#  ------------------------------------Crypto Convert-----------------------------------------------


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crypto_deposit_balance_view(request, *args, **kwargs):
    try:
        with transaction.atomic():
            # {"fromAdd":"a","toAdd":"b","tokenId":1,"quantity":1}
            qs = User.objects.select_for_update().filter(username=request.user)[0].profile
            if qs is not None:
                serializer = CryptoLedgerSerializer(
                    data={"tokenId": request.data.get("tokenId"), "quantity": request.data.get("quantity")})
                if serializer.is_valid(raise_exception=True):
                    CryptoDepositService.execute({
                        'username': request.user,
                        'toAdd': request.data.get("toAdd"),
                        'tokenId': request.data.get("tokenId"),
                        'quantity': request.data.get("quantity"),

                    })
                return Response({"Deposit successful."}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"Something went wrong. Please try again later."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_crypto_balance_view(request, *args, **kwargs):
    try:
        qs = CryptoLedger.objects.filter(user=request.user)
        crypto_data = []
        for i in qs:
            serializer = CryptoSerializer(i)
            crypto_data.append(serializer.data)
        return Response(crypto_data, status=200)
    except Exception as e:
        print(e)
        return Response({"Something went wrong. Please try again later."}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def transfer(request,  *args, **kwargs):
#     with transaction.atomic():

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def transfer(request, *args, **kwargs):
#     try:
#         with transaction.atomic():
#             # {"toAdd": "b", "amount": 1}
#             qs = User.objects.select_for_update().filter(username=request.user)[0].profile
#             if qs is not None:
#                 serializer = TransferLedgerSerializer(
#                     data={"amount": request.data.get("amount"), "toAdd": request.data.get("toAdd")})
#                 if serializer.is_valid(raise_exception=True):
#                     TransferService.execute({
#                         'username': request.user,  # from user
#                         'toAdd': request.data.get("toAdd"),
#                         'amount': request.data.get("amount"),
#                     })
#                 return Response({"transfer successful."}, status=status.HTTP_200_OK)
#     except Exception as e:
#         print(e)
#         return Response({"Something went wrong. Please try again later."}, status=status.HTTP_404_NOT_FOUND)
