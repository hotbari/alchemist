from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from club.models import Club
from team.models import Team
from tier.models import Tier
from image_url.models import ImageUrl
from core.models import SoftDeleteModel , TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator

# CustomUserManager 정의 (CustomUser모델을 사용하려면 필수적으로 필요한 매니저)
class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('birth', 1900)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)


from core.choices import Gender

# 사용자 정의 사용자 커스텀 모델
class CustomUser(AbstractBaseUser, PermissionsMixin, SoftDeleteModel, TimeStampedModel):
    gender = models.CharField(max_length=6,
                              choices=Gender.choices,
                              blank=True,
                              null=True)
    birth = models.IntegerField(
        validators=[
            MinValueValidator(1900, message="Birth year must be 1900 or later"), # 필드의 값이 설정된 최소값 이상
            MaxValueValidator(2050, message="Birth year must be 2050 or earlier") # 필드의 값이 설정된 최대값 이하
        ])
    username = models.CharField(max_length=255) 
    phone = models.CharField(max_length=11, unique=True)
    auth = models.CharField(max_length=255, blank=True, null=True)

    # relationships
    club = models.ForeignKey(
        Club,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='members') # 사용자가 클럽에 속하지 않아도 되며, 사용자 입력 폼에서도 클럽 필드를 비워둘 수 있음
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='members')
    tier = models.ForeignKey(
        Tier,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='users')
    image_url = models.ForeignKey(
        ImageUrl,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='users')

    # ADMINISTRATIVE
    is_active = models.BooleanField(default=True) # is_active 활용하여, 계정을 비활성화 가능 (유저 삭제 대신 False)
    is_staff = models.BooleanField(default=False) # 관리자 페이지 접속 가능하게 하는 staff 기능

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone' # USERNAME_FIELD 로 지정된 값을 흔히 말하는 로그인 ID로 사용됨.
    REQUIRED_FIELDS = [] # 슈퍼유저 생성시 요구되는 필드 목록 설정


    def __str__(self):
        return f"{self.username},({self.phone})"
    

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']