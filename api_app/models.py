from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    profile_photo = models.ImageField(default="default.png", upload_to='profile_photos')


def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


post_save.connect(user_did_save, sender=User)


# class INRTransaction(models.Model):
#     user = models.CharField(max_length=10)
#     balance = models.FloatField(default=0.0)
#     deposit = models.FloatField(default=0.0)
#     withdraw = models.FloatField(default=0.0)
#     dateTime = models.DateTimeField(auto_now_add=True, null=True)

class Book(models.Model):
    book_name = models.CharField(max_length=20)

    def __str__(self):
        return self.book_name


class INRTransaction(models.Model):
    user = models.CharField(max_length=10)
    balance = models.FloatField(default=0.0)
    deposit = models.FloatField(default=0.0)
    deposit_to = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
    # deposit_to = models.CharField(max_length=30,null=True)
    deposit_from = models.CharField(max_length=30, default='bank')
    withdraw = models.FloatField(default=0.0)
    withdraw_to = models.CharField(max_length=30, default='bankW')
    withdraw_from = models.CharField(max_length=30, default='walletD')
    dateTime = models.DateTimeField(auto_now_add=True, null=True)


class CryptoLedger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # fromAdd = models.CharField(max_length=10, default="hi")
    toAdd = models.CharField(max_length=10, default="hi")
    tokenId = models.IntegerField()
    quantity = models.FloatField()
    dateTime = models.DateTimeField(auto_now_add=True, null=True)

# class TransferLedger(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # fromAdd = models.CharField(max_length=10, default="hi")
#     toAdd = models.CharField(max_length=10, default="hi")
#     amount = models.IntegerField()
#     dateTime = models.DateTimeField(auto_now_add=True, null=True)
