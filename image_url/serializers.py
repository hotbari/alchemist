from rest_framework import serializers
from .models import ImageUrl

class ClubImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUrl
        fields = ('image',)
