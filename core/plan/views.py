from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from . import permissions
from . import models
from .serializers import ExerciseSerializer, PlanSerializer


class ExerciseViewSet(ModelViewSet):
    '''ViewSet for Exercise model.'''
    serializer_class = ExerciseSerializer
    queryset = models.Exercise.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated,
                                       permissions.IsCoachUser]
            return [permission() for permission in self.permission_classes]

        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated,
                                       IsAdminUser,
                                       permissions.IsCoachUser]
            return [permission() for permission in self.permission_classes]

        self.permission_classes = [IsAuthenticated, permissions.IsCoachUser]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by == request.user or request.user.is_staff:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.created_by == request.user and request.user.is_coach:
            return super().update(request, *args, **kwargs)

        return Response(
            'You do not have permission to perform such an action.',
            status=status.HTTP_403_FORBIDDEN
            )

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.created_by == request.user and request.user.is_coach:
            return super().partial_update(request, *args, **kwargs)

        return Response(
            'You do not have permission to perform such an action.',
            status=status.HTTP_403_FORBIDDEN
            )


class PlanViewSet(ModelViewSet):
    '''ViewSet for Plan model.'''
    serializer_class = PlanSerializer
    queryset = models.Plan.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated,
                                       permissions.IsCoachUser]
            return [permission() for permission in self.permission_classes]

        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated,
                                       permissions.IsCoachUser]
            return [permission() for permission in self.permission_classes]

        self.permission_classes = [IsAuthenticated, permissions.IsCoachUser]
        return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = models.Plan.objects.filter(coach=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.coach == request.user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response(
            'Only the coach of the plan can retrieve it.',
            status=status.HTTP_403_FORBIDDEN,
            )

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
        obj = self.get_object()
        if obj.coach == request.user or request.user.is_staff:
            return super().destroy(request, *args, **kwargs)

        return Response(
            'You do not have permission to perform such an action.',
            status=status.HTTP_403_FORBIDDEN,
            )
