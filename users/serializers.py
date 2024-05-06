from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model , authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Club


User = get_user_model()


## 회원가입 부분 serializer ##

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all(), required=False)
    
    class Meta:
        model = User
        fields = ('phone', 'password', 'username', 'birth', 'gender', 'club')

    def validate_phone(self, value):
        user = User.objects.filter(phone=value)
        if user.exists():
            raise serializers.ValidationError("이미 사용중인 전화번호 입니다.")
        return value
    
    def create(self, validated_data):
        # 2개의 비밀번호 검증은 프론트에서 구현
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
            username=validated_data['username'],
            birth=validated_data.get('birth'),
            gender=validated_data.get('gender'),
            club=validated_data.get('club', None) # club은 회원가입때 필수사항은 아님.
        )
        return user


# 로그인 부분 serializer ##

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'phone'
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['phone'] = user.phone
        
        return token

    def validate(self, attrs):
        # 'username' 대신 'phone'을 사용하여 인증
        authenticate_kwargs = {
            'phone': attrs.get(self.username_field),
            'password': attrs.get('password'),
        }
        
        self.user = authenticate(**authenticate_kwargs)
        if self.user is None or not self.user.is_active:
            raise serializers.ValidationError('로그인에 실패하였습니다. 전화번호와 비밀번호를 확인해 주세요.')
        
        # 토큰 발급
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        
        
        return data