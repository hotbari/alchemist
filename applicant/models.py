from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from applicant_info.models import ApplicantInfo
from users.models import CustomUser

class Applicant(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applicant_id')
    applicant = models.ForeignKey(ApplicantInfo, on_delete=models.CASCADE, related_name='applicant_info')
    
    def __str__(self):
        return f"{self.user.username} - {self.applicant_info.competition.name}"    
    
    
    class Meta:
        db_table = 'applicant'