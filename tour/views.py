from django.shortcuts import render
from rest_framework import generics
from .serializers import *


class TourListView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
