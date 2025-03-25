from django.db import models

class Gender(models.TextChoices):
    MALE = 'male', '남성'
    FEMALE = 'female', '여성'