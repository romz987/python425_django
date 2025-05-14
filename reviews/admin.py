from django.contrib import admin

from reviews.models import Review
# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'dog', 'author', 'created', 'sign_of_review')
