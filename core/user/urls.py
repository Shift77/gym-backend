from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('otp/create/', views.CreateOtpView.as_view(), name='create-otp'),
    path('otp/verify', views.VerifyOtpView.as_view(), name='verify-otp')
]
