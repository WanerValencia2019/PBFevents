from django.urls import path
from rest_framework.routers import DefaultRouter

from published_events_deploy.apps.sales_profile.views import SaleProfileView

router = DefaultRouter()

router.register(viewset=SaleProfileView, basename="sale-profile", prefix="sale_profile")


urlpatterns = router.urls