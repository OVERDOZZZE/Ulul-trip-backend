from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from .models import Tour, Review, Category, Region, Guide, Images


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "is_main images".split()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "id name".split()


class GuideSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Guide
        fields = "id get_initials photo".split()


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "id name".split()


class TourSerializer(serializers.ModelSerializer):
    tour_images = ImageSerializer(many=True, read_only=True)
    guide = GuideSerializer()
    region = RegionSerializer(many=True, read_only=True)
    category = CategorySerializer()
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )

    class Meta:
        model = Tour
        fields = (
            "id title description price guide date_departure date_arrival date_published"
            " region is_hot duration complexity category average_rating quantity_limit"
            " set_actual_limit tour_images slug uploaded_images".split()
        )

        def create(self, validated_data):
            uploaded_data = validated_data.pop("uploaded_images")
            tour = Tour.objects.create(**validated_data)
            for uploaded_item in uploaded_data:
                Images.objects.create(tour=tour, images=uploaded_item)
            return tour


class ShortTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = "id title".split()


class ReviewSerializer(serializers.ModelSerializer):
    author = StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "id text author post rating date_published".split()


class GetTitleSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ("id", "slug", "category", "price", "title")
