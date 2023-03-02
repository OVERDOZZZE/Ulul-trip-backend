from django.contrib import admin
from .models import UserReview
#
#
# # Register your models here.
#
#
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         "email", "username", "name", "is_verified")
#     list_display_links = ("email",)
#     search_fields = ("email", "username")
#     prepopulated_fields = {'slug': ('username',)}
#     readonly_fields = ('password', 'is_verified')
#
#
admin.site.register(UserReview)
