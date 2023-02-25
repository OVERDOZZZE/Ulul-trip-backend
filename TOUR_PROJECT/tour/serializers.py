from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField

from .models import Tour, Review, Category, Region, Guide, Images


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = 'is_main image'.split()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name'.split()


class GuideSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Guide
        fields = 'id get_initials photo'.split()


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = 'id name'.split()


class TourSerializer(serializers.ModelSerializer):
    tour_images = ImageSerializer(many=True)
    guide = GuideSerializer()
    region = RegionSerializer()
    category = CategorySerializer()

    class Meta:
        model = Tour
        fields = 'id title description price guide date_departure date_arrival date_published' \
                 ' region is_hot duration complexity category average_rating quantity_limit' \
                 ' set_actual_limit tour_images slug'.split()


class ShortTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = 'id title'.split()


class ReviewSerializer(serializers.ModelSerializer):
    author = StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = 'id text author post rating date_published'.split()

