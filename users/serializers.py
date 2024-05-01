# serializers.py 또는 어디든 적당한 위치에
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Club

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all(), required=False)
    

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'password2', 'username', 'gender', 'club')

    def validate_phone_number(self, value):
        user = User.objects.filter(phone_number=value)
        if user:
            raise serializers.ValidationError("이미 사용중인 전화번호 입니다.")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise ValidationError("두 암호가 일치하지 않습니다.")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
