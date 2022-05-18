from rest_framework import serializers

from published_events_deploy.apps.sales_profile.models import  Withdrawal, SaleProfile
from published_events_deploy.apps.users.serializers import UserSerializer



class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ('id', 'sale_profile', 'amount_withdrawn', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'sale_profile', 'amount_withdrawn', 'status', 'created_at', 'updated_at')


class SaleProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = SaleProfile
        fields = ('id', 'user', 'amount_available', 'amount_retired', 'last_withdraw')
        read_only_fields = ('id', 'user', 'amount_available', 'amount_retired', 'last_withdraw')