from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model , authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Club
from image_url.models import ImageUrl
from image_url.utils import S3ImageUploader


User = get_user_model()


## 회원가입 부분 serializer ##

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all(), required=False)
    image_file = serializers.ImageField(write_only=True, required=False)  # 이미지 파일을 받기 위해 이미지 모델에 있는 임시 보관소 필드
    image_url = serializers.URLField(read_only=True, allow_blank=True, default=None)
    
    class Meta:
        model = User
        fields = ('phone', 'password', 'username', 'birth', 'gender', 'club', 'image_file', 'image_url')
        

    def validate_phone(self, value):
        user = User.objects.filter(phone=value)
        if user.exists():
            raise serializers.ValidationError("이미 사용중인 전화번호 입니다.")
        return value
    
    def create(self, validated_data):
        # 2개의 비밀번호 검증은 프론트에서 구현
        image_data = validated_data.pop('image_file', None) 
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
            username=validated_data['username'],
            birth=validated_data.get('birth'),
            gender=validated_data.get('gender'),
            club=validated_data.get('club', None) # club은 회원가입때 필수사항은 아님.
        )
        
        if image_data:
            # S3ImageUploader를 사용하여 S3에 이미지 업로드
            image_url, extension, file_size = S3ImageUploader.upload_image_to_s3(image_data)
            # S3에서 이미지URL , 확장자, 이미지 크기(용량) 정보를 가져와서 DB에 저장
            image_instance = ImageUrl.objects.create(
                image_url=image_url,
                extension=extension,
                size=file_size,
            )
            # CustomUser 모델의 image_url 필드를 업데이트하려면 해당 ImageUrl 인스턴스를 참조하도록 설정
            user.image_url = image_instance
            user.save()
        
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
    
        # # 사용자 정보를 JSON 형태로 추가
        # user_info = {
        #     'id': self.user.id,
        #     'phone': self.user.phone,
        #     'username': self.user.username,
        #     'image_url': self.user.image_url.url if self.user.image_url else None,
        # }
        
        # # user가 클럽이 존재한다면 클럽 정보도 추가.
        # if hasattr(self.user, 'club') and self.user.club:
        #     user_info['club'] = {
        #         'id': self.user.club.id,
        #         'name': self.user.club.name
        #     }
        
        # data['user'] = user_info  # user_id(PK) 에 사용자 데이터를 추가했음.
