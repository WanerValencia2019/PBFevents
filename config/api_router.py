from published_events_deploy.apps.users.urls import urlpatterns as user_routes
from published_events_deploy.apps.events.urls import urlpatterns as event_routes

app_name = "api"
urlpatterns = []

# USER ROUTES MANAGEMENT
urlpatterns = []
urlpatterns += user_routes
urlpatterns += event_routes

