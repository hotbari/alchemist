from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from competition.models import Competition



class Applicant(TimeStampedModel, SoftDeleteModel):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='applicants')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    is_waiting = models.BooleanField(default=False)  # 대기 명단 여부