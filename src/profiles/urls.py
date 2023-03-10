from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from src.users.views import VerifyEmailView

router = SimpleRouter()
router.register(
    "change-password",
    views.ProfileChangePasswordViewSet,
    basename="users_change_password",
)
router.register("profile", views.UsersDetailUpdateDelete, basename="update")
urlpatterns = [
    path("", include(router.urls)),
    path("verify-email/", VerifyEmailView.as_view(), name="update_profile"),
    path("<int:id>/favorites/", views.GetFavoriteTourApiView.as_view()),
    path("request-email-validate/", views.RequestEmailValidateApiView.as_view()),
]
