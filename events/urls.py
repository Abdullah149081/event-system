from django.urls import path
from events.views import (
    home,
    event_detail,
    event,
    category_dashboard,
    participant_dashboard,
    create_event,
    update_event,
    delete_event,
    create_participant,
    update_participant,
    delete_participant,
    create_category,
    update_category,
    delete_category,
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
    path("form/create_event/", create_event, name="create_event"),
    path("form/update_event/<int:event_id>/", update_event, name="update_event"),
    path("form/delete_event/<int:event_id>/", delete_event, name="delete_event"),
    path("form/create_participant/", create_participant, name="create_participant"),
    path(
        "form/update_participant/<int:participant_id>/",
        update_participant,
        name="update_participant",
    ),
    path(
        "form/delete_participant/<int:participant_id>/",
        delete_participant,
        name="delete_participant",
    ),
    path("form/create_category/", create_category, name="create_category"),
    path(
        "form/update_category/<int:category_id>/",
        update_category,
        name="update_category",
    ),
    path(
        "form/delete_category/<int:category_id>/",
        delete_category,
        name="delete_category",
    ),
] + debug_toolbar_urls()  # Include Debug Toolbar URLs if installed
