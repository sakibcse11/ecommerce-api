from django.db.models import Count
from rest_framework import viewsets, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

from apps.common.permissions import IsAdmin, IsVendor, IsNotAuthenticated
from .models import Vendor
from .serializers import VendorSerializer, VendorDetailSerializer, VendorUpdateSerializer

# Create your views here.

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'products_count']

    def get_queryset(self):
        queryset = Vendor.objects.all().annotate(
            products_count=Count('products')
        )

        # If the user is not an admin, only show active vendors
        if not self.request.user.is_authenticated or not self.request.user.is_admin:
            queryset = queryset.filter(is_active=True)

        return queryset

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]

        elif self.action in ['create']:
            permission_classes = [IsNotAuthenticated]

        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsVendor]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):

        if self.action == 'retrieve':
            return VendorDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return VendorUpdateSerializer
        return self.serializer_class


