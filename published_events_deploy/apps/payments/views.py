import hashlib
import uuid

from django.conf import settings
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView


class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        account_id = settings.PAYU_ACCOUNT_ID
        merchant_id = settings.PAYU_MERCHANT_ID
        api_key = settings.PAYU_API_KEY
        response_url = settings.PAYU_RESPONSE_URL
        confirm_url = settings.PAYU_CONFIRM_URL

        email = "valenciawaner@gmail.com"
        buyer_full_name = "Waner Valencia"
        phone = "3205959194"
        algorithm_signature = "MD5"
        currency = "COP"
        tax_return_base = 0
        tax = 0
        amount = 1204000
        reference_code = uuid.uuid4().hex[0:6].upper()
        description = "Compra de articulos"
        test = "0"
        payment_signature = hashlib.md5(
            f"{api_key}~{merchant_id}~{reference_code}~{amount}~{currency}".encode()).hexdigest()

        next_url = settings.API_LOCAL_BASE_URL + f"/payment/confirm?account_id={account_id}&merchant_id={merchant_id}&reference_code={reference_code}&amount={amount}&money={currency}&buyer_full_name={buyer_full_name}&email={email}&phone={phone}&test={test}&tax={tax}&tax_return_base={tax_return_base}&description={description}&payment_signature={payment_signature}&algorithm_signature={algorithm_signature}&confirm_url={confirm_url}&response_url={response_url}".replace(" ", "%20")

        return Response({"message": "Orden creada con éxito", "next_url": next_url}, status=200)


class PaymentConfirmView(View):

    def get(self, request, *args, **kwargs):
        data = {"account_id": request.GET.get("account_id"), "merchant_id": request.GET.get("merchant_id"),
                "reference_code": request.GET.get("reference_code"), "amount": request.GET.get("amount"),
                "money": request.GET.get("money"), "buyer_full_name": request.GET.get("buyer_full_name"),
                "email": request.GET.get("email"), "phone": request.GET.get("phone"), "test": request.GET.get("test"),
                "tax": request.GET.get("tax"), "tax_return_base": request.GET.get("tax_return_base"),
                "description": request.GET.get("description"),
                "payment_signature": request.GET.get("payment_signature"),
                "algorithm_signature": request.GET.get("algorithm_signature"),
                "confirm_url": request.GET.get("confirm_url"), "response_url": request.GET.get("response_url"),
                "action": settings.PAYU_TEST_URL
                }
        return render(request, 'payment.html', context={"pay": data})
