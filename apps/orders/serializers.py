from rest_framework import serializers
from django.db import transaction

from apps.products.models import Product
from apps.products.serializers import ProductDetailSerializer
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product'
    )
    product_details = ProductDetailSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'quantity', 'price', 'subtotal', 'product_details']
        read_only_fields = ['price', 'subtotal']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product'
    )

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_email = serializers.EmailField(source='customer.email', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_email', 'created_at', 'updated_at',
            'status', 'shipping_address', 'billing_address', 'total_amount', 'items'
        ]
        read_only_fields = ['customer', 'created_at', 'updated_at', 'total_amount']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['shipping_address', 'billing_address', 'items']

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        customer = self.context['request'].user

        order = Order.objects.create(customer=customer, **validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            if product.inventory < quantity:
                raise serializers.ValidationError(f"Not enough stock for {product.name}. Available: {product.inventory}")

            #if the same product, update quantity instead of create another order item
            existing_item = OrderItem.objects.filter(order=order, product=product).first()

            if existing_item:
                existing_item.quantity += quantity
                existing_item.save()
            else:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=item_data['quantity']
                )

            product.inventory -= item_data['quantity']
            product.save()

        order.save()

        return order