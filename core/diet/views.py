from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from plan.permissions import IsCoachUser
from .serializers import DietSerializer
from .models import Diet


class DietViewSet(ModelViewSet):
    '''ViewSet for Diet model.'''
    serializer_class = DietSerializer
    queryset = Diet.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsCoachUser]
            return [permission() for permission in self.permission_classes]

        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsCoachUser]
            return [permission() for permission in self.permission_classes]

        self.permission_classes = [IsAuthenticated, IsCoachUser]
        return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = Diet.objects.filter(coach=request.user)
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
            'Only the coach of the Diet can retrieve it.',
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


#  class FoodViewSet(ModelViewSet):
#     '''ViewSet for Food model.'''
#     serializer_class = FoodSerializer
#     queryset = Food.objects.all()

#     def get_permissions(self):
#         if self.action == 'list' or self.action == 'retrieve':
#             self.permission_classes = [IsAuthenticated, IsCoachUser]
#             return [permission() for permission in self.permission_classes]

#         elif self.action == 'destroy':
#             self.permission_classes = [IsAuthenticated, IsCoachUser]
#             return [permission() for permission in self.permission_classes]

#         self.permission_classes = [IsAuthenticated, IsCoachUser]
#         return [permission() for permission in self.permission_classes]

#     def perform_create(self, serializer):
#         return serializer.save(created_by=self.request.user)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.created_by == request.user or request.user.is_staff:
#             self.perform_destroy(instance)
#             return Response(status=status.HTTP_204_NO_CONTENT)

#         return Response(status=status.HTTP_403_FORBIDDEN)

#     def update(self, request, *args, **kwargs):
#         obj = self.get_object()
#         if obj.created_by == request.user and request.user.is_coach:
#             return super().update(request, *args, **kwargs)

#         return Response(
#             'You do not have permission to perform such an action.',
#             status=status.HTTP_403_FORBIDDEN
#             )

#     def partial_update(self, request, *args, **kwargs):
#         obj = self.get_object()
#         if obj.created_by == request.user and request.user.is_coach:
#             return super().partial_update(request, *args, **kwargs)

#         return Response(
#             'You do not have permission to perform such an action.',
#             status=status.HTTP_403_FORBIDDEN
#             )
