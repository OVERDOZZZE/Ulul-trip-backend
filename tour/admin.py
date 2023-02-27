from django.contrib import admin
from .models import *
# Register your models here.


class TourAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Tour)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Place)
admin.site.register(Images)
