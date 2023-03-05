from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("email-verify/", views.VerifyEmailView.as_view(), name="email-verify"),
    path("login/", views.LoginView.as_view(), name="login"),
    path(
        "password-reset/<uidb64>/<token>/",
        views.PasswordTokenCheckView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "request-reset-email/",
        views.RequestResetPasswordEmailView.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset-complete/",
        views.SetNewPasswordView.as_view(),
        name="password-reset-complete",
    ),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="verify"),
    path('google-login/', views.main)
]
