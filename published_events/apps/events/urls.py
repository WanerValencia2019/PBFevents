from django.urls import path
from rest_framework.routers import DefaultRouter

from published_events.apps.events.views import EventView, ListEvents

router = DefaultRouter()

router.register(viewset=ListEvents, basename="events", prefix="events/list")
router.register(viewset=EventView, basename="event", prefix="events")

urlpatterns = router.urls

