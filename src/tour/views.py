from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tour, Review, Category, Region, Guide
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    GuideSerializer,
    TourSerializer,
    ReviewSerializer,
    RegionSerializer,
    CategorySerializer,
    GetTitleSlugSerializer,
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
    serializer_class = TourSerializer
    search_fields = ("^title",)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# class ReviewListView(generics.ListAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer


# class ReviewCreateView(APIView):
#     def post(self, request, id):
#         post = Tour.objects.get(id=id)
#         Review.objects.create(
#             author=request.user,
#             post_id=id,
#             text=request.data['text'],
#             rating=request.data['rating']
#         )
#         return Response({'review': "Review was created successfully!"})
#
#     permission_classes = [permissions.IsAuthenticated]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


@api_view(["GET"])
def tour_list_view(request, slug):
    tour = Tour.objects.filter(slug=slug)
    serializer = TourSerializer(tour, many=True)
    return Response(data=serializer.data)


class GetSlugTitleListView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = GetTitleSlugSerializer
