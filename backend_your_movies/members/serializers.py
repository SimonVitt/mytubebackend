from rest_framework import serializers
from members.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=4, write_only=True)
    password2 = serializers.CharField(min_length=4, write_only=True)
    
    class Meta:
        model= User
        fields=['email', 'username', 'password1', 'password2']
        
    def validate(self, attrs):
        password1 = attrs.pop('password1', None)
        password2 = attrs.pop('password2', None)
        if password1 != password2:
            raise serializers.ValidationError('password arent the same')
        attrs['password'] = password1        
        return super().validate(attrs)
    
    def create(self, validated_data):
        instance = User.objects.create_user(email=validated_data.get('email'), username=validated_data.get('username'), password=validated_data.get('password'))
        return instance
    
class LoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=500)
    password = serializers.CharField(max_length=500, write_only=True)
    username = serializers.CharField(read_only=True)
    tokens = serializers.CharField(read_only = True)
    publickey = serializers.CharField(read_only=True)
    
    class Meta:
        model=User
        fields = ['email', 'password', 'username', 'tokens', 'publickey']
        
    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        
        user=auth.authenticate(email=email, password=password)
        
        if not user:
            raise AuthenticationFailed('credetials not right')
        if not user.is_active:
            raise AuthenticationFailed('Account not active')
        
        attrs['username'] = user.username
        attrs['tokens'] = user.tokens()
        attrs['publickey'] = settings.SIMPLE_JWT['VERIFYING_KEY']
        
        return super().validate(attrs)
    
class ResetPasswordSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model=User
        fields = ['password1', 'password2']
        
    def validate(self, attrs):
        password1 = attrs.pop('password1', None)
        password2 = attrs.pop('password2', None)
        if password1 != password2:
            raise serializers.ValidationError('password arent the same')
        attrs['password'] = password1
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email') 