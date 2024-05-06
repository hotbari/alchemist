from django.db import models

class Competition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=6, blank=True, null=True)
    start_date = models.DateTimeField(db_column='startDate', blank=True, null=True)
    end_date = models.DateTimeField(db_column='endDate', blank=True, null=True)  
    round = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    rule = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    code = models.BigIntegerField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True) # 대회 참가비 변수명 바꿔야할듯
    bank_name = models.CharField(db_column='bankName', max_length=30, blank=True, null=True) 
    bank_account_number = models.IntegerField(db_column='bankAccountNumber', blank=True, null=True)  
    bank_account_name = models.CharField(db_column='bankAccountName', max_length=30, blank=True, null=True)  
    site_link = models.TextField(db_column='siteLink', blank=True, null=True)  
    feedback = models.CharField(max_length=255, blank=True, null=True)
    # match_type = models.ForeignKey('MatchType', models.DO_NOTHING)
    # tier = models.ForeignKey('Tier', models.DO_NOTHING)

    class Meta:
        db_table = 'competition'
