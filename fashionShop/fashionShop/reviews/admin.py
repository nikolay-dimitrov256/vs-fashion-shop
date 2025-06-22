from django.contrib import admin

from fashionShop.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
