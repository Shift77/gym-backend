from django.contrib import admin
from .models import Diet, Routine


class RoutineInline(admin.StackedInline):
    '''Inline of Routine model.'''
    model = Routine
    extra = 1


@admin.register(Diet)
class Diet(admin.ModelAdmin):
    '''Diet admin panel config.'''
    model = Diet
    inlines = [RoutineInline]


admin.site.register(Routine)
# admin.site.register(Food)
