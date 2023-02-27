from django.contrib import admin
from .models import Tour, Category, Region, Review, Images, Guide

# Register your models here.


class TourAdmin(admin.ModelAdmin):
    search_fields = "title description".split()
    list_display_links = ["title"]
    list_display = "title price date_departure region guide complexity duration average_rating".split()
    list_editable = "price date_departure".split()
    ordering = ["date_departure"]
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 10
    list_filter = (
        "region category date_departure is_hot duration complexity guide".split()
    )


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class GuideAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ReviewAdmin(admin.ModelAdmin):
    search_fields = "author post".split()
    list_display = "author post rating date_published".split()
    ordering = ["rating"]
    list_filter = "date_published rating".split()
    list_per_page = 10


admin.site.register(Tour, TourAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Images)
admin.site.register(Guide, GuideAdmin)
