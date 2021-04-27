from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name']

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']

class ForgetPasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'email']
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=60, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'confirm_password']

class UserShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
