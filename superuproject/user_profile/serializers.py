from rest_framework import serializers
from .models import User, UserInfo
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alpha numeric characters')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=5)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=5, read_only=True)
    tokens = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Please enter valid credentials')
        if not user.is_active:
            raise AuthenticationFailed('Please check the active status of the account')
        if not user.is_verified:
            raise AuthenticationFailed('Please finish email verification')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }


class UserProfileSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(max_length=10)
    user_bio = serializers.CharField(max_length=255)
    occupation = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    pincode = serializers.CharField(max_length=7)

    class Meta:
        model = UserInfo
        fields = ['mobile_number', 'user_bio', 'occupation', 'city', 'pincode']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField(max_length=10, required=False)
    user_bio = serializers.CharField(max_length=255, required=False)
    occupation = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=255, required=False)
    pincode = serializers.CharField(max_length=7, required=False)

    class Meta:
        model = UserInfo
        fields = ['mobile_number', 'user_bio', 'occupation', 'city', 'pincode']
