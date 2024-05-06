from django.db import models
from core.models import TimeStampedModel


class ImageUrl(TimeStampedModel):
    id = models.IntegerField(primary_key=True,)
    image = models.ImageField(upload_to='images/', max_length=255, blank=True, null=True)  # AWS S3에 저장될 경로 설정
    IMAGE_TYPES = (
        ('user', '유저이미지'),
        ('club', '클럽이미지'),
        ('team', '팀이미지'),
        ('competition', '대회이미지'),
    )
    image_type = models.CharField(max_length=30, choices=IMAGE_TYPES)
    user = models.ForeignKey('users.CustomUser', on_delete=models.DO_NOTHING, null=True, blank=True)
    club = models.ForeignKey('club.Club', on_delete=models.DO_NOTHING, null=True, blank=True)
    team = models.ForeignKey('team.Team', on_delete=models.DO_NOTHING, null=True, blank=True)
    competition = models.ForeignKey('competition.Competition', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.get_image_type_display()
    
    class Meta:
        db_table = 'image_url'



# class ImageUrl(TimeStampedModel):
#     id = models.IntegerField(primary_key=True)
#     profile_image = models.ImageField(upload_to='images/', max_length=255, blank=True, null=True)  # AWS S3에 저장될 경로 설정
    
    
#     user = models.ForeignKey('users.CustomUser', on_delete=models.DO_NOTHING, null=True, blank=True)
#     club = models.ForeignKey('club.Club', on_delete=models.DO_NOTHING, null=True, blank=True)
#     team = models.ForeignKey('team.Team', on_delete=models.DO_NOTHING, null=True, blank=True)
#     competition = models.ForeignKey('competition.Competition', on_delete=models.DO_NOTHING, null=True, blank=True)

#     def __str__(self):
#         return self.get_image_type_display()
    
#     class Meta:
#         db_table = 'image_url'