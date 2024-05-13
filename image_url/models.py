from django.db import models
from core.models import TimeStampedModel


class ImageUrl(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=1024, blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    size = models.IntegerField(null=True, blank=True)
    

    class Meta:
        db_table = 'image_url'

    def __str__(self):
        return f"{self.id} - {self.image_url if self.image_url else 'No Image'}"
