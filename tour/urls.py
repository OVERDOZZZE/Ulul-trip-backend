from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'tours', TourViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),

]
