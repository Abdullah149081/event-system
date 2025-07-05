from django.urls import path
from events.views import home, event_detail, event
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path("", home, name="home"),
    path("event/eventDetails/<int:event_id>/", event_detail, name="event_details"),
    path("/events/", event, name="event"),
] + debug_toolbar_urls()  # Include Debug Toolbar URLs if installed
