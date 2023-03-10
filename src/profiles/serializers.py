from django.contrib.auth import password_validation
from rest_framework import serializers
from src.users.models import User
from src.tour.models import Tour
from rest_framework.validators import UniqueValidator


class ProfileEditSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(
        max_length=30,
        min_length=2,
        required=True,
        help_text="Name should contain only alphabetical characters",
    )
    first_name = serializers.CharField(
        max_length=30,
        min_length=2,
        required=True,
        help_text="Username should contain only alphanumeric characters",
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]

    def validate(self, attrs):
        last_name = attrs.get("last_name", "")
        first_name = attrs.get("first_name", "")
        if not last_name.isalpha():
            raise serializers.ValidationError(
                f"The users last_name  should only contain alphabetical characters"
            )
        if not first_name.isalpha():
            raise serializers.ValidationError(
                f"The users first_name  should only contain alphabetical characters",
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


class FavoriteTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    favorite_tour = FavoriteTourSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "favorite_tour")


class AddToFavoriteSerializer(serializers.ModelSerializer):
    favorite_tour = serializers.SlugRelatedField(slug_field=Tour.slug, read_only=True)

    class Meta:
        model = Tour
        fields = ("favorite_tour",)


class RequestEmailValidateSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
