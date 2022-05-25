from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from published_events_deploy.apps.sales_profile.models import SaleProfile, Withdrawal

from published_events_deploy.apps.sales_profile.serializers import SaleProfileSerializer, WithdrawalSerializer

from rest_framework.viewsets import ViewSetMixin


def get_withdraws(sale_profile):
    return Withdrawal.objects.filter(sale_profile=sale_profile)
    

class SaleProfileView(ViewSetMixin, ListAPIView):
    serializer_class = SaleProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = SaleProfile.objects.all()


    def list(self, request, *args, **kwargs):
        user = request.user
        try :
            sale_profile = SaleProfile.objects.get(user=user)
            sale_profile_data = SaleProfileSerializer(instance=sale_profile).data
            print(sale_profile_data)
            withdraws = get_withdraws(sale_profile)
            withdraws_data = WithdrawalSerializer(instance=withdraws, many=True).data
            print(withdraws_data)
            sale_profile_data['withdraws'] = withdraws_data
            return Response({"data": sale_profile_data},  status=200)
        except SaleProfile.DoesNotExist:
            return Response({'message': ['Aún no tienes cuenta de pagos, crea tu primer evento']}, status=404)

        
class WithdrawalView(ViewSetMixin, CreateAPIView):
    serializer_class = SaleProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = SaleProfile.objects.all()


    def post(self, request, *args, **kwargs):
        user = request.user
        try :
            sale_profile = SaleProfile.objects.get(user=user)
            amount_withdrawn = request.data['amount_withdrawn']
            if amount_withdrawn > sale_profile.amount_available:
                return Response({'message': ['No tienes suficiente dinero para retirar']}, status=404)
            else:
                withdraw = Withdrawal()
                withdraw.sale_profile = sale_profile
                withdraw.amount_withdrawn = amount_withdrawn
                withdraw.save()

                sale_profile.amount_available -= amount_withdrawn
                sale_profile.amount_retired += amount_withdrawn
                sale_profile.last_withdraw = timezone.now()
                sale_profile.save()
                return Response({'message': ['Retiro realizado']}, status=200)
                
            return Response({"data": sale_profile_data},  status=200)
        except SaleProfile.DoesNotExist:
            return Response({'message': ['Aún no tienes cuenta de pagos, crea tu primer evento']}, status=404)