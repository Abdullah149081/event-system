from django.urls import path
from events.views import (
    show_event,
)
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path("show/", show_event, name="show_event"),
] + debug_toolbar_urls()  # Include Debug Toolbar URLs if installed
