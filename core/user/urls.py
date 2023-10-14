from django.urls import path
from .views import CreatePendingUserView

app_name = 'user'
urlpatterns = [
    path('create/', CreatePendingUserView.as_view(), name='create-user'),
]
