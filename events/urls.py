from django.urls import path
from events.views import home
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path("", home, name="home"),
] + debug_toolbar_urls()  # Include Debug Toolbar URLs if installed
