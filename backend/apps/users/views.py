from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)

from .serializers import UserSerializer, MyTokenObtainPairSerializer
from .models import User


class SignUpAPIView(APIView):
    permission_classes = ()

    default_serializer_class = UserSerializer

    def get_serializer_class(self, key=None):
        return self.serializer_classes.get(key, self.default_serializer_class)

    def post(self, request):
        data = request.data

        if 'user_type' in data:
            user_type = data.pop('user_type')
            if user_type == User.SUPER_ADMIN:
                data['is_superuser'] = True
            elif user_type == User.STAFF:
                data['is_staff'] = True
            else:
                data['is_customer'] = True
        
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = serializer.data
        data['token'] = user.get_tokens()

        return Response({
            'message': 'User has been created successfully',
            'data': data
        }, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)