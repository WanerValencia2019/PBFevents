from django.urls import path
from rest_framework.routers import DefaultRouter

from published_events_deploy.apps.payments.views import PaymentConfirmPayu, PaymentView, GeneratePaymentView, PayFreeEvent

urlpatterns = [
    path('payment', GeneratePaymentView.as_view(), name="payment"),
    path('payment/free', PayFreeEvent.as_view(), name="payment-free"),
    path("payment/confirm", PaymentView.as_view(), name="payment_confirm"),
    path("payment/payu/confirm", PaymentConfirmPayu.as_view(), name="payment_payu_confirm"),
    path("payment/payu/response", PaymentConfirmPayu.as_view(), name="payment_payu_response"),
]
