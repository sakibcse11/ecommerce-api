from rest_framework import serializers
from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    products_count = serializers.IntegerField(read_only=True)
    logo = serializers.ImageField(required=False)
    banner = serializers.ImageField(required=False)
    class Meta:
        model = Vendor
        fields = [
            'id', 'name', 'slug', 'description', 'user_email', 'user_name',
            'logo', 'banner', 'is_active',
            'created_at', 'updated_at', 'products_count'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return Vendor.objects.create(user=user, **validated_data)

class VendorDetailSerializer(VendorSerializer):
    products = serializers.SerializerMethodField()

    class Meta(VendorSerializer.Meta):
        fields = VendorSerializer.Meta.fields + ['products']

    def get_products(self, obj):
        from apps.products.serializers import ProductListSerializer
        from apps.products.models import Product

        products = Product.objects.filter(vendor=obj)[:5]
        return ProductListSerializer(products, many=True, context=self.context).data


class VendorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'description', 'logo', 'banner']
