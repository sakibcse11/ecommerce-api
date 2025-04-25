from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Prefetch

from apps.common.permissions import IsCustomer, IsVendor, IsAdmin
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'customer__email', 'status']
    ordering_fields = ['created_at', 'updated_at', 'total_amount']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action in ['create', 'my_orders']:
            permission_classes = [IsCustomer]
        elif self.action in ['list', 'retrieve','update_status']:
            permission_classes = [IsAdmin]
        elif self.action in ['vendor_orders']:
            permission_classes = [IsVendor]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('product'))
        )

        if user.is_staff or hasattr(user, 'admin'):
            return queryset

        if hasattr(user, 'vendor'):
            vendor = user.vendor
            return queryset.filter(items__product__vendor=vendor).distinct()

        return queryset.filter(customer=user)

    #Admin can update status of an order
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        status = request.data.get('status')

        if status not in [choice[0] for choice in Order.STATUS_CHOICES]:
            return Response(
                {'error': 'Invalid status value'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status
        order.save()

        return Response(OrderSerializer(order).data)

    #Customer orders
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        orders = Order.objects.filter(customer=request.user).prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('product'))
        )

        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    #vencor can see their orders
    @action(detail=False, methods=['get'])
    def vendor_orders(self, request):
        if not hasattr(request.user, 'vendor'):
            return Response(
                {'error': 'Only vendors can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )

        vendor = request.user.vendor
        orders = Order.objects.filter(
            items__product__vendor=vendor
        ).prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('product').filter(product__vendor=vendor))
        ).distinct()

        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)