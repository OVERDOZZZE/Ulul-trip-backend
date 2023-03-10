from django.urls import path, include
from .views import *
from rest_framework import routers
from src.profiles.views import FavoriteTourApiView
router = routers.SimpleRouter()
router.register(r"review", ReviewViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("tours/", TourListView.as_view(), name="tour_list"),
    path("guides/", GuideListView.as_view(), name="guides"),
    path("regions/", RegionListView.as_view(), name="regions"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("tours/<slug:slug>/", tour_list_view, name="tour-list"),
    path("tours/<str:slug>/favorite/", FavoriteTourApiView.as_view(), name="favorites-crud")
    # path('src/v1/reviews/create/<int:id>', ReviewCreateView.as_view(), name='review_create')
    # path('src/v1/reviews/', ReviewListView.as_view(), name='reviews'),
]
