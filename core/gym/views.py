from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import GymSerializer, ReviewSerializer
from .models import Gym, Review


class GymViewset(viewsets.ModelViewSet):
    serializer_class = GymSerializer
    permission_classes = [AllowAny, IsAdminUser]
    model = Gym
    queryset = Gym.objects.all()

    def get_permissions(self):
        '''Getting permission for different methods.'''
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [AllowAny]
            return [permission() for permission in self.permission_classes]

        self.permission_classes = [IsAdminUser]

        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        context = {'user': self.request.user}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class ReviewViewset(viewsets.ModelViewSet):
    '''Viewset for review model.'''
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [AllowAny]
            return [permission() for permission in self.permission_classes]

        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        context = {'user': self.request.user}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.author == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.author == request.user:
            return super().update(request, *args, **kwargs)

        return Response('Bad request!', status=status.HTTP_400_BAD_REQUEST)
