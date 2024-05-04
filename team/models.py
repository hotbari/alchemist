from django.db import models
from club.models import Club
from image_url.models import ImageUrl
from core.models import TimeStampedModel

class Team(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    club = models.ForeignKey(Club, models.DO_NOTHING)
    image_url = models.ForeignKey(ImageUrl, models.DO_NOTHING)

    class Meta:
        db_table = 'team'