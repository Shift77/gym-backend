from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    '''View to create a user.'''
    serializer_class = UserSerializer


class ProfileView(RetrieveUpdateAPIView):
    '''Retrieve and update the user.'''
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
