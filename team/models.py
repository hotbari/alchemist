from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel

class Team(TimeStampedModel, SoftDeleteModel):
    # id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    club = models.ForeignKey('club.Club', models.SET_NULL, blank=True, null=True)
    image_url = models.ForeignKey('image_url.ImageUrl', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'team'