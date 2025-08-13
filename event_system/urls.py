from django.contrib import admin
from django.urls import path, include
from events.views import home, dashboard
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("users/", include("users.urls")),
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    try:
        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    except ImportError:
        pass


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
