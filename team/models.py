from django.db import models
from core.models import TimeStampedModel

class Team(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    club = models.ForeignKey('club.Club', models.DO_NOTHING)

    class Meta:
        db_table = 'team'