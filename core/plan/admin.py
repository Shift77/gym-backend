from django.contrib import admin
from . import models


class ExerciseInline(admin.StackedInline):
    '''Inline Exercise model.'''
    model = models.SubPlan.exercises.through
    extra = 1


class SubPlanInline(admin.StackedInline):
    '''Inline SubPlan model.'''
    model = models.SubPlan
    extra = 1


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    '''Plan model admin.'''
    inlines = [SubPlanInline]


@admin.register(models.SubPlan)
class SubPlanAdmin(admin.ModelAdmin):
    '''Plan model admin.'''
    inlines = [ExerciseInline]


admin.site.register(models.Exercise)
