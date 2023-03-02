from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email-verify/', views.VerifyEmailView.as_view(), name='email-verify'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckView.as_view(), name='password-reset-confirm'),
    path('request-reset-email/', views.RequestResetPasswordEmailView.as_view(), name='request-reset-email'),
    path('password-reset-complete/', views.SetNewPasswordView.as_view(), name='password-reset-complete'),
]