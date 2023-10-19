from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('gym', views.GymViewset)

review_router = DefaultRouter()
review_router.register('review', views.ReviewViewset)

app_name = 'gym'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(review_router.urls))
]
