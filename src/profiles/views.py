from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from src.users.models import User
from .serializers import (
    ProfileEditSerializer,
    ChangePasswordSerializer,
)
from rest_framework import permissions
from src.users.utils import Util


# Create your views here.
class ProfileEditViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ProfileEditSerializer
    lookup_field = "id"
    http_method_names = ("put",)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = request.user.email
        user = User.objects.get(email=email)
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")
        absurl = "http://" + current_site + relative_link + "?token=" + str(token)
        email_body = (
                "Hi "
                + user.first_name.title()
                + "! "
                + " Use link below to verify your email\n"
                + absurl
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }
        Util.send_email(data)
        first_name = serializer.validated_data.get("first_name", "")
        last_name = serializer.validated_data.get("last_name", "")
        email_new = serializer.validated_data.get("email", "")
        user.first_name = first_name
        user.last_name = last_name
        user.email = email_new
        user.save()
        return Response(
            data=self.serializer_class(user).data, status=status.HTTP_201_CREATED
        )


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


class DeleteAccount(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()

        return Response({"result": "user delete"}, status=status.HTTP_204_NO_CONTENT)
# class DeleteProfileView(ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'id'
#     http_method_names = ('delete',)
#     serializer_class = DeleteProfileSerializer
#
#     def delete(self, request, *args, **kwargs):
#         serializer = DeleteProfileSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user_id = request.user.id
#         user = User.objects.get(user_id=user_id)
#         password = serializer.validated_data.get("password")
#         check_password = user.check_password(password=password)
#         if check_password:
#             user.delete()
#             return Response(
#                 {
#                     "Removed successfully.": "Your account has been successfully deleted.",
#                 },
#                 status=status.HTTP_204_NO_CONTENT,
#             )
#         else:
#             return Response(
#                 {
#                     "Error!": "The password entered is incorrect.",
#                 },
#                 status=status.HTTP_406_NOT_ACCEPTABLE,
#             )
