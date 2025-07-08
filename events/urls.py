from django.urls import path
from events.views import (
    home,
    event_detail,
    event,
    category_dashboard,
    participant_dashboard,
)
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path("", home, name="home"),
    path("event/eventDetails/<int:event_id>/", event_detail, name="event_details"),
    path("dashboard/EventDashboard", event, name="event"),
    path(
        "dashboard/ParticipantDashboard",
        participant_dashboard,
        name="participant_dashboard",
    ),
    path("dashboard/CategoryDashboard", category_dashboard, name="category_dashboard"),
] + debug_toolbar_urls()  # Include Debug Toolbar URLs if installed
