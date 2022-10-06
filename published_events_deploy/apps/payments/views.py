import hashlib
import threading
from uuid import uuid4


from django.utils import timezone
from django.conf import settings
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from published_events_deploy.apps.transactions.actions import cancel_transaction, create_transaction, pay_transaction
from published_events_deploy.apps.events.models import Event, TicketType
from published_events_deploy.apps.transactions.models import Transaction
from published_events_deploy.utils.mails import send_ticket_mail


class GeneratePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        account_id = settings.PAYU_ACCOUNT_ID
        merchant_id = settings.PAYU_MERCHANT_ID
        api_key = settings.PAYU_API_KEY
        response_url = settings.PAYU_RESPONSE_URL
        confirm_url = settings.PAYU_CONFIRM_URL

        data: dict = request.data
        email = data.get("email", None)
        buyer_full_name = data.get("full_name", None)
        phone = data.get("phone", None)
        ticket_id: str = data.get("ticket_type_id", None)
        ticket_quantity: int = data.get("ticket_quantity", None)
        identification:str = data.get("identification", None) 

        if not email:
            return Response({"message": "email es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        elif not buyer_full_name:
            return Response({"message": "full_name es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        elif not phone:
            return Response({"message": "phone es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        elif not ticket_id:
            return Response({"message": "ticket_type_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        elif not ticket_quantity:
            return Response({"message": "ticket_quantity es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        amount = None
        ticket_type: TicketType = None
        try:
            ticket_type = TicketType.objects.get(id=ticket_id)

            event:Event = ticket_type.event

            if(event.sell_limit_date < timezone.now()):
                return Response({"message": "El evento ya no esta disponible para la venta"}, status=status.HTTP_400_BAD_REQUEST)

            if not (ticket_type.availables - ticket_type.ticket_sales) >= ticket_quantity:
                return Response({"message": "La cantidad de entradas excede las permitidas"},
                                status=status.HTTP_400_BAD_REQUEST)
            amount = ticket_type.unit_price * ticket_quantity
        except ObjectDoesNotExist as ex:
            return Response({"message": "El ticket no es válido"}, status=status.HTTP_400_BAD_REQUEST)

        algorithm_signature = "MD5"
        currency = "COP"
        tax_return_base = 0
        tax = 0
        reference_code = ticket_id.upper()[0:12]+uuid4().hex[0:12]
        description = f"Compra de {ticket_quantity} entradas {ticket_type.name} para el evento '{ticket_type.event.title}'"
        test = "0"
        payment_signature = hashlib.md5(
            f"{api_key}~{merchant_id}~{reference_code}~{amount}~{currency}".encode()).hexdigest()

        payment_result = {
            "status": "CREATED",
            "email" : email,
            "buyer_full_name":buyer_full_name,
            "phone" : phone,
            "ticket_quantity": ticket_quantity,
            "amount": amount,
            "identification": identification,
            "reference_code": reference_code,
        }
        transaction = create_transaction(identification, ticket_type, ticket_quantity, payment_result)
        print(transaction)

        next_url = settings.API_PRODUCTION_BASE_URL + f"/payment/confirm?account_id={account_id}&merchant_id={merchant_id}&reference_code={reference_code}&amount={amount}&money={currency}&buyer_full_name={buyer_full_name}&email={email}&phone={phone}&test={test}&tax={tax}&tax_return_base={tax_return_base}&description={description}&payment_signature={payment_signature}&algorithm_signature={algorithm_signature}&confirm_url={confirm_url}&response_url={response_url}".replace(
            " ", "%20")

        return Response({"message": "Orden creada con éxito", "next_url": next_url}, status=200)


class PaymentView(View):
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
        return render(request, 'payment/payment.html', context={"pay": data})


class PaymentConfirmPayu(View):
    def get(self, request, *args, **kwargs):
        """
        It checks if the transaction was approved, if it was, it recovers the transaction and sends the
        ticket to the user, if not, it cancels the transaction
        
        :param request: The request object
        :return: The response is being returned in the form of a dictionary.
        """
        data = request.GET
        transaction = Transaction.objects.filter(id=data.get("referenceCode")).select_related("ticket_type").first()
        STATUS = data.get("lapResponseCode")
        print(transaction)
        print(data.get("referenceCode"))
        if STATUS == "APPROVED":
            transaction_recover, assistant = pay_transaction(transaction)
            if transaction_recover and assistant:
                threading.Thread(target=send_ticket_mail, args=(transaction_recover.ticket_type.event, assistant, transaction_recover)).start()
            return render(request, 'payment/payu_confirm.html', context={"pay": data})
        else:
            cancel_transaction(transaction)
            return render(request, 'payment/payment_error.html', context={"pay": data})
class PaymentResponsePayu(View):
    def get(self, request, *args, **kwargs):
        data = request.GET
        return render(request, 'payment/payu_response.html', context={"pay": data})



class PayFreeEvent(APIView):
    def post(self, request, *args, **kwargs):
        """
        It creates a transaction and returns the transaction id
        
        :param request: The request object
        :return: A transaction object
        """

        data: dict = request.data
        email = data.get("email", None)
        buyer_full_name = data.get("full_name", None)
        phone = data.get("phone", None)
        ticket_id: str = data.get("ticket_type_id", None)
        ticket_quantity: int = data.get("ticket_quantity", None)
        identification:str = data.get("identification", None) 

        if not email:
            return Response({"message": "email es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        elif not buyer_full_name:
            return Response({"message": "full_name es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        elif not phone:
            return Response({"message": "phone es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        elif not ticket_id:
            return Response({"message": "ticket_type_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        elif not ticket_quantity:
            return Response({"message": "ticket_quantity es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        amount = None
        ticket_type: TicketType = None

        

        try:
            ticket_type = TicketType.objects.get(id=ticket_id)

            event:Event = ticket_type.event

            if(event.sell_limit_date < timezone.now()):
                return Response({"message": "El evento ya no esta disponible para la venta"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not ticket_type.unit_price == 0:
                return Response({"message": "El ticket no es gratis"}, status=status.HTTP_400_BAD_REQUEST)
            


            if not (ticket_type.availables - ticket_type.ticket_sales) >= ticket_quantity:
                return Response({"message": "La cantidad de entradas excede las permitidas"},
                                status=status.HTTP_400_BAD_REQUEST)
            amount = ticket_type.unit_price * ticket_quantity
        except ObjectDoesNotExist as ex:
            return Response({"message": "El ticket no es válido"}, status=status.HTTP_400_BAD_REQUEST)

        payment_result = {
            "status": "CREATED",
            "email" : email,
            "buyer_full_name":buyer_full_name,
            "phone" : phone,
            "ticket_quantity": ticket_quantity,
            "amount": amount,
            "identification": identification,
        }
        transaction = create_transaction(identification, ticket_type, ticket_quantity, payment_result)

        if not transaction:
            return Response({"message": "No se pudo realizar la reserva, contacta al administrador"}, status=status.HTTP_400_BAD_REQUEST)
        
        transaction_recover, assistant = pay_transaction(transaction)

        if transaction_recover and assistant:
            threading.Thread(target=send_ticket_mail, args=(transaction_recover.ticket_type.event, assistant, transaction_recover)).start()

        return Response({"message": "Felicidades, tu reserva se ha realizado", "transaction": transaction.id}, status=status.HTTP_200_OK)