from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Tour, Category, Review, Images, Place


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text autor'.split()


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text post autor'.split()


class TourSerializer(serializers.ModelSerializer):
    tour_reviews = ReviewSerializer(many=True)

    class Meta:
        model = Tour
        fields = 'id tour_review title image price'.split()


class TourDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = 'id title description price image category date_published date_departure date_arrival from_place to' \
                 'quantity_limit actual_limit is_hot duration complexity'.split()


class PlaceSerializer(serializers.ModelSerializer):
    from_place = TourSerializer(many=True)
    to = TourSerializer(many=True)

    class Meta:
        model = Place
        fields = 'id from_place to name_city name_place'.split()


class PlaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = 'id name_city name_place'.split()


class CategorySerializer(serializers.ModelSerializer):
    tour_category = TourSerializer(many=True)

    class Meta:
        model = Category
        fields = 'id tour_category name image'.split()


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name image'.split()


class ImageSerializer(serializers.ModelSerializer):
    image_of_tour = TourSerializer(many=True)

    class Meta:
        model = Images
        fields = 'id image_of_tour image'.split()


class ImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = 'id image'.split()
