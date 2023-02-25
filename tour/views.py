from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.viewsets import GenericViewSet

from .serializers import *
from rest_framework import filters
from .service import TourFilter


class TourViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TourFilter

    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    search_fields = 'title'
    lookup_field = 'slug'
