from django.contrib import admin
from django.urls import path, include
from events.views import home, dashboard
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("users/", include("users.urls")),
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("__reload__/", include("django_browser_reload.urls")),
] + debug_toolbar_urls()


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
