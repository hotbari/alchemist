from rest_framework import serializers
from .models import Competition
from matchtype.serializers import MatchTypeSerializer
from image_url.serializers import ImageUrlSerializer



''' 대회 부분 '''

class CompetitionListSerializer(serializers.ModelSerializer):
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    image_url = serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'match_type_details', 'tier', 'location','image_url']
        
    
    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None

    def get_tier(self, obj):
        if obj.image_url:
            return obj.tier.name
        return None


class CompetitionSerializer(serializers.ModelSerializer):
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'end_date', 'tier', 'round', 'description', 'rule',
                  'address', 'location', 'code', 'phone', 'fee', 'bank_name',
                  'bank_account_number', 'bank_account_name', 'site_link', 'feedback',
                  'image_url', 'match_type_details']
    
    
    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None