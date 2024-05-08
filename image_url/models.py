from django.db import models
from core.models import TimeStampedModel
import boto3
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
import os


class InMemoryUploadStorage(FileSystemStorage):
    """데이터베이스에 저장되지 않는 임시 파일 저장소"""
    def get_available_name(self, name, max_length=None):
        return name


class ImageUrl(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    size = models.IntegerField(null=True, blank=True)
    image_file = models.ImageField(storage=InMemoryUploadStorage(), upload_to='temp/', null=True, blank=True)

    class Meta:
        db_table = 'image_url'

    def __str__(self):
        return f"{self.id} - {self.image_url if self.image_url else 'No Image'}"
