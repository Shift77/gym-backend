from django.urls import path, include
from rest_framework import routers
from .views import ExerciseViewSet, PlanViewSet

router = routers.DefaultRouter()
router.register('exercise', ExerciseViewSet)
router.register('', PlanViewSet)


app_name = 'plan'

urlpatterns = [
    path('', include(router.urls)),
]
