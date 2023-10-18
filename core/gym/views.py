from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import GymSerializer
from .models import Gym


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
