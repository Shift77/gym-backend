from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DietViewSet

router = DefaultRouter()
# router.register('food', FoodViewSet)
router.register('', DietViewSet)

app_name = 'diet'

urlpatterns = [
    path('', include(router.urls))
]
