from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView
    )
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, OtpSerializer, VerifyOtpSerializer


class CreateUserView(CreateAPIView):
    '''View to create a user.'''
    serializer_class = UserSerializer


class ProfileView(RetrieveUpdateAPIView):
    '''Retrieve and update the user.'''
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CreateOtpView(UpdateAPIView):
    '''View for creating and verifying otp for phone number of the user.'''
    serializer_class = OtpSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Otp sent to your phone number.', status=200)


class VerifyOtpView(CreateAPIView):
    serializer_class = VerifyOtpSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        context = {'request.user': self.request.user}
        serializer = VerifyOtpSerializer(
            request.user,
            data=request.data,
            context=context)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Your phone number is now verified!', status=202)
