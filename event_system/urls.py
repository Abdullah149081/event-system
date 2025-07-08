from django.contrib import admin
from django.urls import path, include
from events.views import home, dashboard
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
