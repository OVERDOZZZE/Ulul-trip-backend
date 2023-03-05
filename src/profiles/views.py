from rest_framework import status, exceptions
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from src.users.models import User
from .serializers import (
    ProfileEditSerializer,
    ChangePasswordSerializer,
)
from rest_framework import permissions

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
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = User.objects.all()
    http_method_names = ("put","patch","delete")


