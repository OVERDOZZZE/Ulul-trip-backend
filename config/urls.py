from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from .settings.drf_yasg import urlpatterns

admin.site.site_header = "Моя админка"
admin.site.index_title = "Мои модели"

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("user/", include("src.user.urls")),
    path("tour/", include("src.tour.urls")),
    path("auth/", include("rest_framework.urls")),
    path("local/", include("django.conf.urls.i18n")),
    *urlpatterns,
]
