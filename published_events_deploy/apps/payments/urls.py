from django.urls import path
from rest_framework.routers import DefaultRouter

from published_events_deploy.apps.payments.views import PaymentConfirmPayu, PaymentView, GeneratePaymentView

urlpatterns = [
    path('payment', GeneratePaymentView.as_view(), name="payment"),
    path("payment/confirm", PaymentView.as_view(), name="payment_confirm"),
    path("payment/payu/confirm", PaymentConfirmPayu.as_view(), name="payment_payu_confirm"),
    path("payment/payu/response", PaymentConfirmPayu.as_view(), name="payment_payu_response"),
]
