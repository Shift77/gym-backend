from django.contrib import admin
from . import models

admin.site.register(models.Review)
admin.site.register(models.Social)


class ReviewInline(admin.StackedInline):
    model = models.Review
    readonly_fields = ['id']
    extra = 1


class SocialInline(admin.StackedInline):
    model = models.Social
    readonly_fields = ['id']
    extra = 1


@admin.register(models.Gym)
class GymAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, SocialInline]
