from django.db import models
from core.models import TimeStampedModel

class ImageUrl(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.TextField(db_column='imageUrl', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'image_url'
