from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tour import views

urlpatterns = {
    path('admin/', admin.site.urls),
    path('api/v1/tours', views.TourListCreateAPIView.as_view()),
    path('api/v1/tours/<int:id>/', views.TourDetailAPIView.as_view()),
    path('api/v1/review', views.ReviewModelViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('api/v1/review/<int:id>/', views.ReviewModelViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    })),
}
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
