from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from image_url.models import  ImageUrl
from matchtype.models import MatchType
from tier.models import Tier

class Competition(TimeStampedModel, SoftDeleteModel):
    STATUS_CHOICES = (
        ('before', 'before'),
        ('during', 'during'),
        ('ended', 'ended'),
    )

    # 대회 유형에 리그 추가
    TYPE_CHOICES = (
        ('tournament', '토너먼트'),
        ('league', '리그'),
    )

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES) # 날짜 인식해서 자동으로 상태변경 로직 필요
    name = models.CharField(max_length=30, blank=True, null=True)
    start_date = models.DateTimeField(db_column='startDate', blank=True, null=True)
    end_date = models.DateTimeField(db_column='endDate', blank=True, null=True)  
    total_rounds = models.IntegerField(blank=True, null=True)
    total_sets = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    rule = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True) # 대회 참가비 변수명 바꿔야할듯
    bank_name = models.CharField(db_column='bankName', max_length=30, blank=True, null=True) 
    bank_account_number = models.CharField(db_column='bankAccountNumber', max_length=30, blank=True, null=True) # CharField로 수정
    bank_account_name = models.CharField(db_column='bankAccountName', max_length=30, blank=True, null=True)  
    site_link = models.TextField(db_column='siteLink', blank=True, null=True)  
    image_url = models.ForeignKey(ImageUrl, on_delete=models.DO_NOTHING, blank=True, null=True)
    match_type = models.ForeignKey(MatchType, models.DO_NOTHING)
    tier = models.ForeignKey(Tier, models.DO_NOTHING)
    max_participants = models.IntegerField(default=0)
    deposit_date = models.IntegerField(null=True, help_text="입금기한_신청기준 몇일")
    competition_type = models.CharField(max_length=10, choices=TYPE_CHOICES) # 추가
    
    
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'competition'




