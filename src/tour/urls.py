from django.urls import path, include
from .views import *
from rest_framework import routers
from src.profiles.views import FavoriteTourApiView

router = routers.SimpleRouter()
router.register(r"review", ReviewViewSet, basename="review")
router.register(r'tour', TourDetail, basename='tour')

urlpatterns = [
    path("", include(router.urls)),
    path("slugs/", GetSlugTitleListView.as_view(), name="slugs"),
    path("tours/", TourListView.as_view(), name="tour_list"),
    path("guides/", GuideListView.as_view(), name="guides"),
    path("regions/", RegionListView.as_view(), name="regions"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path(
        "tours/<str:slug>/favorite/",
        FavoriteTourApiView.as_view(),
        name="favorites-crud",
    ),
    path('tours/<int:tour_id>/reviews/', TourReviewsList.as_view()),
    path('about_us/', AboutUsList.as_view())
]
