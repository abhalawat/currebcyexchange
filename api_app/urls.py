from django.urls import path

from .views import CryptoTransactionViewSet, show_crypto_balance_view, show_balance_view, deposit_balance_view, withdraw_balance_view, \
    crypto_deposit_balance_view

urlpatterns = [
    path('view/', show_balance_view),
    path('deposit/', deposit_balance_view),
    path('withdraw/', withdraw_balance_view),
    path('crypto_trans/', crypto_deposit_balance_view),
    path('crypto_view/', show_crypto_balance_view),
    path('journal/', show_balance_view),
    # path('transfer/', transfer),

]
