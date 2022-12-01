from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def welcome(req):
    return Response("Welcome To abra exercise DRF. First register in users/register, Then get authentication token from users/get-token")