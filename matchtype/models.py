from django.db import models
from core.models import TimeStampedModel

class MatchType(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    type = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        db_table = 'match_type'
