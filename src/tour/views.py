from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Tour, Review, Category, Region, Guide, AboutUs
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    GuideSerializer,
    TourSerializer,
    ReviewSerializer,
    RegionSerializer,
    CategorySerializer,
    GetTitleSlugSerializer,
    AboutUsSerializer,
    ShortTourSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from .service import TourFilter
from rest_framework.filters import SearchFilter, OrderingFilter


class GuideListView(generics.ListAPIView):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer


class TourListView(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = TourFilter
    queryset = Tour.objects.all()
    serializer_class = ShortTourSerializer
    search_fields = ("^title",)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class TourDetail(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get(self.lookup_field)
        if slug:
            queryset = queryset.filter(slug=slug)
        return queryset


class GetSlugTitleListView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = GetTitleSlugSerializer


class TourReviewsList(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        tour = Tour.objects.get(slug=slug)
        return Review.objects.filter(post=tour)


class AboutUsList(generics.ListAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
