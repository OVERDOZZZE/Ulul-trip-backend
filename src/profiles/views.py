from rest_framework import status, exceptions, permissions, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from src.users.models import User
from .exceptions import UserNotFoundException, TourNotFoundException
from .serializers import (
    ProfileEditSerializer,
    ChangePasswordSerializer,
    AddToFavoriteSerializer,
    ProfileSerializer,
    RequestEmailValidateSerializer,
)
from src.tour.models import Tour
from .services import ProfileService


class ProfileChangePasswordViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    lookup_field = "id"
    http_method_names = ("patch",)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.user.email
        user = User.objects.get(email=email)
        password_new_again = serializer.validated_data.get("password_new_again")
        password_old = serializer.validated_data.get("password_old")
        password_new = serializer.validated_data.get("password_new")
        password_check = user.check_password(password_old)
        if not password_check:
            raise exceptions.ValidationError("Old password is not valid")
        if password_new != password_new_again:
            raise exceptions.ValidationError(
                "Password new and Password new again should be the same"
            )
        user.set_password(password_new_again)
        user.save()
        return Response(
            data=self.serializer_class(user).data, status=status.HTTP_201_CREATED
        )


class UsersDetailUpdateDelete(ModelViewSet):
    serializer_class = ProfileEditSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    http_method_names = ("put", "get", "delete")

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(id=request.user.id)
            ProfileService.send_email(
                user=user, email=serializer.validated_data.get("email")
            )
            user.first_name = serializer.validated_data.get("first_name")
            user.last_name = serializer.validated_data.get("last_name")
            user.email = serializer.validated_data.get("email")
            user.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class FavoriteTourApiView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = AddToFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        try:
            user = get_object_or_404(User, id=request.user.id)
            serializer = ProfileSerializer(user, many=False)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except:
            raise UserNotFoundException()

    def post(self, request, slug):
        try:
            user = request.user
            tour = get_object_or_404(Tour, slug=slug)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                ProfileService.add_to_favorite(user, tour)
                return Response("Ok")
            return Response(serializer.errors)
        except:
            raise TourNotFoundException()

    def delete(self, request, slug):
        try:
            user = request.user
            tour = get_object_or_404(Tour, slug=slug)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                ProfileService.remove_from_favorite(user, tour)
                return Response("Ok")
            return Response(serializer.errors)
        except:
            raise TourNotFoundException()


class GetFavoriteTourApiView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = self.serializer_class(user, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            raise UserNotFoundException()


class RequestEmailValidateApiView(generics.GenericAPIView):
    serializer_class = RequestEmailValidateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def send(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(id=request.user.id)
            email = serializer.validated_data.get("email")
            ProfileService.send_email(user, email)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            user = User.objects.get(id=request.user.id)
            if user.is_verified:
                user.email = email
                user.save()
            else:
                user.email = request.user.email
                user.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
