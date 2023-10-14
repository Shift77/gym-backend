from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from . import serializers

class CreatePendingUserView(CreateAPIView):
    '''
    View for sending otp to their provided phone number to verify.
    '''
    serializer_class = serializers.PendingSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'success': True,
             'message': 'OTP was sent for verification.'
             },
             status=200
            )
