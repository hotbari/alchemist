from django.db import models
from match_type.models import MatchType
from core.models import TimeStampedModel, SoftDeleteModel
class Tier(TimeStampedModel, SoftDeleteModel):
    name = models.CharField(max_length=6, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    match_type = models.ForeignKey(MatchType, models.DO_NOTHING)

    class Meta:
        db_table = 'tier'
