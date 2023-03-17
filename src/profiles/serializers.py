from django.contrib.auth import password_validation
from rest_framework import serializers
from src.users.models import User
from src.tour.models import Tour
from src.tour.serializers import TourSerializer
from rest_framework.validators import UniqueValidator


class FavoriteTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = "__all__"


class ProfileEditSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=30,
        min_length=2,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text="Username should contain only alphanumeric characters",
    )
    email = serializers.EmailField(required=True)
    favorite_tour = FavoriteTourSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "favorite_tour")

    def validate(self, attrs):
        username = attrs.get("username", "").split(' ')
        for name in username:
            if not name.isalpha() or (name.isalpha() and len(username) != 2):
                raise serializers.ValidationError(
                    f"The users username: {name} should only contain alphabetical characters ex: Ivan Ivanov",
                    400,
                )
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password_old = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
    )
    password_new_again = serializers.CharField(
        required=True,
        write_only=True,
        validators=[password_validation.validate_password],
        style={"input_type": "password"},
    )
    password_new = serializers.CharField(
        max_length=30,
        min_length=6,
        write_only=True,
        required=True,
        help_text=password_validation.password_validators_help_texts(),
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ("email", "password_old", "password_new", "password_new_again")


class ProfileSerializer(serializers.ModelSerializer):
    favorite_tour = TourSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "favorite_tour")


class AddToFavoriteSerializer(serializers.ModelSerializer):
    favorite_tour = serializers.SlugRelatedField(slug_field=Tour.slug, read_only=True)

    class Meta:
        model = Tour
        fields = ("favorite_tour",)


class RequestEmailValidateSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
