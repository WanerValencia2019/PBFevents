from django.urls import path
from rest_framework.routers import DefaultRouter

from published_events_deploy.apps.events.views import EventView, ListEvents, DetailEvent, NearEvents

router = DefaultRouter()

router.register(viewset=DetailEvent, basename="event-detail", prefix="event/detail")
router.register(viewset=ListEvents, basename="events", prefix="events/list")
router.register(viewset=EventView, basename="event", prefix="events")
router.register(viewset=NearEvents, basename="event", prefix="events/nearby")
urlpatterns = router.urls

