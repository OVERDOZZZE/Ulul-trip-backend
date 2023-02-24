from django.urls import path
from .views import *


urlpatterns = [
    path('api/v1/tours/', TourListView.as_view(), name='tour_list'),

]
