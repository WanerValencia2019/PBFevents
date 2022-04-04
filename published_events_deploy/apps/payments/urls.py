from django.urls import path
from rest_framework.routers import DefaultRouter

from published_events_deploy.apps.payments.views import PaymentView, PaymentConfirmView

urlpatterns = [
    path('payment', PaymentView.as_view(), name="payment"),
    path("payment/confirm", PaymentConfirmView.as_view(), name="payment_confirm"),
]
