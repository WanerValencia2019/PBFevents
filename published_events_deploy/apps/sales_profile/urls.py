from django.urls import path
from rest_framework.routers import DefaultRouter

from published_events_deploy.apps.sales_profile.views import SaleProfileView, WithdrawalView

router = DefaultRouter()

router.register(viewset=SaleProfileView, basename="sale-profile", prefix="sale_profile")
router.register(viewset=WithdrawalView, basename="withdrawal", prefix="withdrawal")



urlpatterns = router.urls