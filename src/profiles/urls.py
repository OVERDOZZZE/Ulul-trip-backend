from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from src.users.views import VerifyEmailView

router = SimpleRouter()
router.register("update", views.ProfileEditViewSet, basename="users_edit")
router.register(
    "change-password",
    views.ProfileChangePasswordViewSet,
    basename="users_change_password",
)
urlpatterns = [
    path("", include(router.urls)),
    path("verify-email/", VerifyEmailView.as_view(), name="update_profile"),
    path("delete-profile/",views.DeleteAccount.as_view(),name="delete_profile")
]
