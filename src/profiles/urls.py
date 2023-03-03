from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register("update",views.ProfileEditViewSet, basename="users_edit")
router.register("change-password",views.ProfileChangePasswordViewSet, basename="users_change_password")
urlpatterns = [
    path('',include(router.urls))
]
