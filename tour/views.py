from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Tour, Review, Place, Category, Images
from .serializers import TourSerializer, ReviewSerializer, CategorySerializer, PlaceSerializer, ImageSerializer
from rest_framework.pagination import PageNumberPagination


class TourListCreateAPIView(ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer


class TourDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    lookup_field = 'id'


# class TourListCreateAPIView(ListCreateAPIView):
#     queryset = Tour.objects.all()
#     serializer_class = TourSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = TourSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(data={'errors': serializer.errors},
    #                         status=status.HTTP_406_NOT_ACCEPTABLE)
    #     title = serializer.validated_data.get('title')
    #     description = serializer.validated_data.get('description')
    #     price = serializer.validated_data.get('price')
    #     image = serializer.validated_data.get('image')
    #     category = serializer.validated_data.get('category')
    #     slug = serializer.validated_data.get('slug')
    #     from_place = serializer.validated_data.get('from_place')
    #     to = serializer.validated_data.get('to')
    #     duration = serializer.validated_data.get('duration')
    #     complexity = serializer.validated_data.get('complexity')
    #
    #     movie = Tour.objects.create(title=title, description=description, price=price, image=image, category=category,
    #                                 slug=slug, from_place=from_place, to=to, duration=duration, complexity=complexity)
    #     movie.save()
    #     return Response(data=TourDetailSerializer(movie).data, status=status.HTTP_201_CREATED)


class ReviewModelViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class PlaceModelViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class ImageModelViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
