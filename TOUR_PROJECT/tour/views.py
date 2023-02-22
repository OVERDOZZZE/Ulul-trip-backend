from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tour, Review, Category, Region, Guide
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from .service import TourFilter


class GuideListView(generics.ListAPIView):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer


class TourListView(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TourFilter

    queryset = Tour.objects.all()
    serializer_class = TourSerializer


class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewCreateView(APIView):
    def post(self, request, id):
        post = Tour.objects.get(id=id)
        Review.objects.create(
            author=request.user,
            post_id=id,
            text=request.data['text'],
            rating=request.data['rating']
        )
        return Response({'review': "Review was created successfully!"})

    permission_classes = [permissions.IsAuthenticated]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


@api_view(['GET'])
def tour_list_view(request, slug):
    tour = Tour.objects.filter(slug=slug)
    serializer = TourSerializer(tour, many=True)
    return Response(data=serializer.data)
