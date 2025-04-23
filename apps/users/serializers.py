from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

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
