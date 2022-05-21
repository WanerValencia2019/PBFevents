from django.urls import path
from rest_framework.routers import DefaultRouter

from published_events_deploy.apps.events.views import CategoriesView, CreateEventView, EventView, ListEvents, DetailEvent, NearEvents,VerifyAssistant, MyAssistantsView

router = DefaultRouter()

router.register(viewset=DetailEvent, basename="event-detail", prefix="event/detail")
router.register(viewset=ListEvents, basename="events", prefix="events/list")
router.register(viewset=VerifyAssistant, basename="event-assistant", prefix="events/assistant")
router.register(viewset=MyAssistantsView, basename="event-assistant", prefix="events/assistant/me")
router.register(viewset=NearEvents, basename="events", prefix="events/nearby")
router.register(viewset=CreateEventView, basename="events", prefix="events/create")
router.register(viewset=CategoriesView, basename="events-categories", prefix="events/categories")
router.register(viewset=EventView, basename="event", prefix="events")



urlpatterns = router.urls

