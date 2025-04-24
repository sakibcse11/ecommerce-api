from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, generics
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers import (
    UserSerializer,
    CustomerRegistrationSerializer,
    AdminRegistrationSerializer, CustomTokenObtainPairSerializer,
)
from apps.common.permissions import IsAdmin, IsNotAuthenticated

User = get_user_model()

# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomerRegistrationView(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [IsNotAuthenticated]

class AdminRegistrationView(generics.CreateAPIView):
    serializer_class = AdminRegistrationSerializer
    permission_classes = [IsAdmin]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        return queryset
