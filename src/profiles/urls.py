from django.urls import path
from . import views

get_post = {'get': 'list',
            'post': 'create'}
get_put_delete = {'get': 'retrieve',
                  'put': 'update',
                  'delete': 'destroy'}
urlpatterns = [
    path('<slug:slug>/', views.ProfileEditViewSet.as_view(get_put_delete)),
    path('<slug:slug>/update/', views.ProfileEditViewSet.as_view(get_put_delete)),
    path('<slug:slug>/change-password/', views.ProfileChangePasswordViewSet.as_view(get_put_delete)),
    path('<slug:slug>/review/', views.ProfileReviewUpdateViewSet.as_view(get_put_delete))
]
