from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'review', ReviewViewSet)


urlpatterns = [
    path('api/v1/tours/', TourListView.as_view(), name='tour_list'),
    path('api/v1/', include(router.urls)),
    # path('api/v1/reviews/', ReviewListView.as_view(), name='reviews'),
    path('api/v1/guides/', GuideListView.as_view(), name='guides'),
    path('api/v1/regions/', RegionListView.as_view(), name='regions'),
    path('api/v1/categories/', CategoryListView.as_view(), name='categories'),

    path('api/v1/tours/<slug:slug>/', tour_list_view, name='tour-list'),
    # path('api/v1/reviews/create/<int:id>', ReviewCreateView.as_view(), name='review_create')

]
