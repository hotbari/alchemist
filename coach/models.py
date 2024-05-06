from django.db import models
from club.models import Club
from users.models import CustomUser

class Coach(models.Model):
    id = models.IntegerField(primary_key=True)
    club = models.ForeignKey(Club, models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, models.DO_NOTHING)

    class Meta:
        db_table = 'coach'