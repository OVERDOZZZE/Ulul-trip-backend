from django.shortcuts import render
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from src.users.models import User
from .serializers import (
    ProfileEditSerializer,
    ChangePasswordSerializer,
    ProfileReviewSerializer,
    ProfileReviewUpdateSerializer
)

from .models import UserReview
from rest_framework import permissions


# Create your views here.
class ProfileEditViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ProfileEditSerializer
    lookup_field = 'user_slug'

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_username = request.user.username
        name = serializer.validated_data.get('name')
        username = serializer.validated_data.get('username')
        number = serializer.validated_data.get('number')
        image = serializer.validated_data.get('image')
        user = User.objects.get(username=old_username)
        user.name = name
        user.username = username
        user.number = number
        user.image = image
        user.save()
        return Response(data=self.serializer_class(user).data,
                        status=status.HTTP_201_CREATED)


class ProfileChangePasswordViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    lookup_field = 'user_slug'

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.user.email
        user = User.objects.get(email=email)
        password_new_again = serializer.validated_data.get('password_new_again')
        password_old = serializer.validated_data.get('password_old')
        password_new = serializer.validated_data.get('password_new')
        password_check = user.check_password(password_old)
        if not password_check:
            raise exceptions.ValidationError('Old password is not valid')
        if password_new != password_new_again:
            raise exceptions.ValidationError('Password new and Password new again should be the same')
        user.set_password(password_new_again)
        user.save()
        return Response(data=self.serializer_class(user).data,
                        status=status.HTTP_201_CREATED)


class ProfileReviewViewSet(ModelViewSet):
    queryset = UserReview.objects.all()
    serializer_class = ProfileReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.user.username)
        review = serializer.validated_data.get('review')
        rate = serializer.validated_data.get('rate')
        user_review = UserReview.objects.create(user=user, review=review, rate=rate)
        user_review.save()
        return Response(data=self.serializer_class(user_review).data,
                        status=status.HTTP_201_CREATED)


class ProfileReviewUpdateViewSet(ModelViewSet):
    queryset = UserReview.objects.all()
    serializer_class = ProfileReviewUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=request.user.username)
        review = serializer.validated_data.get('review')
        rate = serializer.validated_data.get('rate')
        user_review = UserReview.objects.get(user=user)
        user_review.review = review
        user_review.rate = rate
        user_review.user = user
        user_review.save()
        return Response(data=self.serializer_class(user_review).data,
                        status=status.HTTP_201_CREATED)
