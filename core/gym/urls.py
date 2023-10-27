from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GymViewset, ReviewViewset

router = DefaultRouter()
router.register('review', ReviewViewset)
router.register('', GymViewset)

app_name = 'gym'

urlpatterns = [
    path('', include(router.urls)),
]
