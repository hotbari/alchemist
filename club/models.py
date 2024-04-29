from django.db import models
from image_url.models import ImageUrl
from core.models import TimeStampedModel

class Club(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.ForeignKey(ImageUrl, models.DO_NOTHING)

    class Meta:
        db_table = 'club'
