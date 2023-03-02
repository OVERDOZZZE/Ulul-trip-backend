from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from .settings.drf_yasg import urlpatterns
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header = "Моя админка"
admin.site.index_title = "Мои модели"

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("user/", include("src.user.urls")),
    path("tour/", include("src.tour.urls")),
    path("auth/", include("rest_framework.urls")),
    path("local/", include("django.conf.urls.i18n")),
    path("users/", include("src.users.urls")),
    path("profiles/", include("src.profiles.urls")),
    *urlpatterns,
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
