from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .serializers import UserCreateSerializer, LoginSerializer
from .models import User
from .services import JWTService


@api_view(['POST'])
@permission_classes([AllowAny])
def createUser(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"detail": "Request Body Error."},
                            status=status.HTTP_409_CONFLICT)

        if User.objects.filter(
                email=serializer.validated_data['email']).first() is None:
            serializer.save()
            return Response({"detail": "ok"},
                            status=status.HTTP_201_CREATED)
        return Response({"detail": "duplicate email"},
                        status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response({"detail": "Request Body Error."},
                        status=status.HTTP_409_CONFLICT)

    if len(User.objects.filter(
            email=serializer.validated_data['email']).values()):
        user = User.objects.get(
            email=serializer.validated_data['email'])
    else:
        return Response({"detail": "User didn't exist."},
                        status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(serializer.validated_data["password"]):
        return Response({"detail": "Email and password is Not Match."},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "access_token": JWTService.create_access_token_with_id(
            user.id, int(request.data['minute']))
        if 'minute' in request.data
        else JWTService.create_access_token_with_id(user.id),
        "refresh_token": JWTService.create_refresh_token_with_id(user.id)
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def refresh(request):
    pk = JWTService.run_auth_process(request.headers, 'refresh')

    return Response({'access_token':
                    JWTService.create_access_token_with_id(pk)},
                    status=status.HTTP_200_OK)
