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
        
        # image_data가 None이 아니고, 파일 크기가 0보다 큰 경우에만 이미지 업로드 실행
        if image_data and hasattr(image_data, 'size') and image_data.size > 0:
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




# 회원정보 수정 serializer
class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all(), required=False)
    image_file = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField(read_only=True)  # 읽기 전용 이미지 URL 필드 추가

    class Meta:
        model = User
        fields = ('password', 'username', 'birth', 'gender', 'club', 'image_file', 'image_url')

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None

    def update(self, instance, validated_data):
        image_data = validated_data.pop('image_file', None)
        password = validated_data.pop('password', None)

        # 사용자 기본 정보 업데이트
        instance.username = validated_data.get('username', instance.username)
        instance.birth = validated_data.get('birth', instance.birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.club = validated_data.get('club', instance.club)

        if password:
            instance.set_password(password)

        # 빈 이미지 파일이 제공된 경우 (이미지 삭제 요청으로 간주)
        if image_data in [None, '']:
            if hasattr(instance, 'image_url') and instance.image_url:
                instance.image_url.delete()  # ImageUrl 인스턴스 삭제
                instance.image_url = None  # User 모델의 참조 제거
        # 유효한 이미지 파일이 제공된 경우
        elif image_data:
            uploader = S3ImageUploader()
            file_url, extension, size = uploader.upload_file(image_data)

            # 기존 이미지가 있으면 업데이트, 없으면 새로 생성
            if hasattr(instance, 'image_url') and instance.image_url:
                instance.image_url.image_url = file_url
                instance.image_url.extension = extension
                instance.image_url.size = size
                instance.image_url.save()
            else:
                image_instance = ImageUrl.objects.create(
                    image_url=file_url,
                    extension=extension,
                    size=size
                )
                instance.image_url = image_instance

        instance.save()
        return instance






# 유저 상세정보 serializer
class UserInfoSerializer(serializers.ModelSerializer):
    image_url = ImageUrlSerializer(read_only=True)  # ImageUrl 모델에 대한 시리얼라이저를 사용
    club = ClubDetailSerializer(read_only=True)
    team = TeamDetailSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'phone', 'gender', 'birth', 'image_url', 'club', 'team'] # 티어 추가해야함