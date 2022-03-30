from tokenize import String

from rest_framework import serializers

from .models import Profile, INRTransaction, CryptoLedger


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # balance should be integer and positive
        balance = serializers.FloatField()

        @staticmethod
        def validate(data):
            balance = data.get('balance')
            if balance < 0.0:
                raise serializers.ValidationError('amount cannot be negative')

        fields = ['balance', ]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = INRTransaction

        # validation for each fields
        @staticmethod
        def validate(data):
            # user
            if data['user'] is not None or String:
                raise serializers.ValidationError('Not valid User')

            # balance
            if data['balance'] is not None or int:
                raise serializers.ValidationError('Not valid balance')
            # deposit
            if data['deposit'] is not None or int:
                raise serializers.ValidationError('Not valid deposit')
            # withdraw
            if data['withdraw'] is not None or int:
                raise serializers.ValidationError('Not valid withdraw')

        fields = ['user', 'balance', 'deposit', 'deposit_to', 'deposit_from', 'withdraw', 'withdraw_to', 'withdraw_from', 'dateTime']


# class AmountSerializer(serializers.Serializer):
#     def create(self, validated_data):
#         pass
#
#     def update(self, instance, validated_data):
#         pass
#
#     amount = serializers.FloatField()
#
#     def validate(self, data):
#
#         if data['amount'] < 0.0:
#             print(data['amount'])
#             raise serializers.ValidationError('amount cannot be none or negative')
#
#         if data['amount'] is None:
#             raise serializers.ValidationError('Amount and target can not be specified together')
#         return data['amount']

class AmountSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    amount = serializers.FloatField()

    def validate(self, data):
        if data['amount'] < 0.0:
            print(data['amount'])
            raise serializers.ValidationError('amount cannot be none or negative')

        if data['amount'] is None:
            raise serializers.ValidationError('Amount and target can not be specified together')
        return data['amount']


class WithdrawSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    amount = serializers.FloatField()
    # balance = serializers.FloatField()

    def validate(self, data):
        # balance = data.get('balance')
        amount = data.get("amount")

        if amount < 0.0:
            raise serializers.ValidationError('amount cannot be none or negative')
        elif amount is None:
            raise serializers.ValidationError('Amount and target can not be specified together')
        # elif amount > balance:
        #     raise serializers.ValidationError('amount is greater then balance ')
        return amount


class CryptoSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    class Meta:
        model = CryptoLedger
        fields = ['toAdd', 'tokenId', 'quantity', 'dateTime']


class CryptoLedgerSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    tokenId = serializers.IntegerField()
    quantity = serializers.FloatField()

    def validate(self, data):
        quantity = data.get('quantity')
        token_id1 = data.get("tokenId")
        print(token_id1, quantity)
        if token_id1 is None or quantity is None:
            raise serializers.ValidationError("tokenId or quantity should not be empty")
        elif token_id1 < 0 or quantity < 0:
            raise serializers.ValidationError("tokenId or quantity should not be empty")
        return quantity, token_id1


# class ShowCryptoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CryptoLedger
#         fields = ['fromAdd', 'toAdd', 'tokenId', 'quantity']

# class TransferLedgerSerializer(serializers.Serializer):
#     def update(self, instance, validated_data):
#         pass
#
#     def create(self, validated_data):
#         pass
#
#     to_add = serializers.CharField()
#     amount = serializers.IntegerField()
#
#     def validate(self, data):
#         amount = data.get('amount')
#         to_add = data.get("to_add")
#
#         if amount < 0.0:
#             raise serializers.ValidationError('amount cannot be none or negative')
#         elif amount is None:
#             raise serializers.ValidationError('Amount and target can not be specified together')
#
#         if not Profile.objects.get(user=to_add):
#             raise serializers.ValidationError('User does not exist')
