from published_events_deploy.apps.users.urls import urlpatterns as user_routes
from published_events_deploy.apps.events.urls import urlpatterns as event_routes
from published_events_deploy.apps.payments.urls import urlpatterns as payment_routes
from published_events_deploy.apps.sales_profile.urls import urlpatterns as sales_profile_routes

app_name = "api"
urlpatterns = []

# USER ROUTES MANAGEMENT
urlpatterns = []
urlpatterns += user_routes
urlpatterns += event_routes
urlpatterns += payment_routes
urlpatterns += sales_profile_routes

