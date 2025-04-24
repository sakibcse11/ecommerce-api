from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Vendor
from ..users.serializers import UserSerializer

User = get_user_model()

class VendorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True,
                                   validators=[UniqueValidator(
                                       queryset=User.objects.all(),
                                       message="Email already exists.")])
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True, required=False)
    address = serializers.CharField(write_only=True, required=False)

    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Vendor
        fields = [
            'id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'address',
            'name', 'slug', 'description', 'logo', 'banner',
            'user_email', 'user_name', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        phone_number = validated_data.pop('phone_number')
        address = validated_data.pop('address')

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
            role='vendor'
        )
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
