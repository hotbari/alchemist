from django.db import models
from django.contrib.auth.models import AbstractUser
from club.models import Club
from team.models import Team
from image_url.models import ImageUrl
from tier.models import Tier
from core.models import TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator


# 사용자 정의 사용자 커스텀 모델
class CustomUser(AbstractUser, TimeStampedModel):
    # 기존 필드(username, email, first_name, last_name 등)는 AbstractUser에서 상속받기 때문에 필드에는 보이지 않음.
    
    # 성별필드에 choices 구현
    GENDER_CHOICES = (
        ('male', '남성'),
        ('female', '여성'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    
    birth = models.IntegerField(
        default = 1980, #필드 기본 값
        validators=[
            MinValueValidator(1900), # 필드의 값이 설정된 최소값 이상
            MaxValueValidator(2050) # 필드의 값이 설정된 최대값 이하
        ])
    
    auth = models.CharField(max_length=20, blank=True, null=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True) # 사용자가 클럽에 속하지 않아도 되며, 사용자 입력 폼에서도 클럽 필드를 비워둘 수 있음
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True) 
    image_url = models.ForeignKey(ImageUrl, on_delete=models.CASCADE, blank=True, null=True) 
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'users'


