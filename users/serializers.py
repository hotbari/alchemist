from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model , authenticate
from rest_framework import serializers
from .models import CustomUser, Club
from image_url.models import ImageUrl
from image_url.utils import S3ImageUploader
from image_url.serializers import ImageUrlSerializer
from club.serializers import ClubDetailSerializer
from team.serializers import TeamDetailSerializer


User = get_user_model()

# 회원가입 부분
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all(), required=False)
    image_file = serializers.ImageField(write_only=True, required=False)  # 이미지 필드 추가
    image_url = serializers.SerializerMethodField(read_only=True)  # 읽기 전용 이미지 URL 필드 추가
    
    class Meta:
        model = User
        fields = ('phone', 'password', 'username', 'birth', 'gender', 'club', 'image_file', 'image_url')
        
    def get_image_url(self, obj):
        if hasattr(obj, 'image_url'):
            return obj.image_url.image_url
        return None

    def create(self, validated_data):
        image_data = validated_data.pop('image_file', None)
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
            username=validated_data['username'],
            birth=validated_data.get('birth'),
            gender=validated_data.get('gender'),
            club=validated_data.get('club', None)
        )
        
        if image_data:
            uploader = S3ImageUploader()
            file_url, extension, size = uploader.upload_file(image_data)
            
            # 업로드된 이미지 정보를 ImageUrl 인스턴스로 저장
            image_instance = ImageUrl.objects.create(
                image_url=file_url,
                extension=extension,
                size=size
            )
            user.image_url = image_instance  # 사용자 인스턴스에 이미지 인스턴스 할당
            user.save()  # 변경 사항 저장
            
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



# 유저 상세정보 serializer
class UserInfoSerializer(serializers.ModelSerializer):
    image_url = ImageUrlSerializer(read_only=True)  # ImageUrl 모델에 대한 시리얼라이저를 사용
    club = ClubDetailSerializer(read_only=True)
    team = TeamDetailSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'phone', 'gender', 'birth', 'image_url', 'club', 'team'] # 티어 추가해야함