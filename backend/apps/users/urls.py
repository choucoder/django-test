from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)

from .views import *


urlpatterns = [
    path('accounts/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/register/', SignUpAPIView.as_view(), name='signup'),
]
