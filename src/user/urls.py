from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    path("src/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("src/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("src/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("src/v1/register-user/", views.register_user, name="register-user"),
    path("activate/<uid64>/<token>", views.activate, name="activate"),
    path(
        "src/v1/request-password-reset/",
        views.PasswordResetView.as_view(),
        name="request-password-reset",
    ),
    path(
        "src/v1/password-reset/<str:encoded_pk>/<str:token>/",
        views.ResetPasswordAPI.as_view(),
        name="reset-password",
    ),
]
