from django.contrib import admin

from .models import Book, Profile, INRTransaction, CryptoLedger

admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(INRTransaction)
# admin.site.register(CryptoTransaction)
admin.site.register(CryptoLedger)


