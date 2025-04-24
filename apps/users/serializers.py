from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role
        return token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'},write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'role',
                  'phone_number', 'address','email',  'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomerRegistrationSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        pass
    def create(self, validated_data):
        validated_data['role'] = 'customer'
        return super().create(validated_data)


class VendorRegistrationSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        pass

    def create(self, validated_data):
        validated_data['role'] = 'vendor'
        user = super().create(validated_data)
        from apps.vendors.models import Vendor
        Vendor.objects.create(user=user)
        return user

class AdminRegistrationSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': False}
        }
    def create(self, validated_data):
        validated_data['role'] = 'admin'
        return super().create(validated_data)
