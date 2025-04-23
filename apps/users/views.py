from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, generics
from rest_framework.request import Request

from apps.users.serializers import (
    UserSerializer,
    CustomerRegistrationSerializer
)
from apps.common.permisions import IsAdmin

User = get_user_model()

# Create your views here.
class CustomerRegistrationView(generics.CreateAPIView):

    serializer_class = CustomerRegistrationSerializer
    permission_classes = [permissions.AllowAny]


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
