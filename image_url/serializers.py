from rest_framework import serializers
from .models import ImageUrl



class ImageUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUrl
        fields = ['id', 'image_url', 'extension', 'size']
