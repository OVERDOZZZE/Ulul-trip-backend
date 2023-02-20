from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tour import views

urlpatterns = {
    path('admin/', admin.site.urls),
    path('api/v1/tours', views.TourListCreateAPIView.as_view()),
    path('api/v1/tours/<slug:tour_slug>/', views.TourDetailAPIView.as_view()),
}
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
