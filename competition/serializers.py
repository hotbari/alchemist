from django.utils.timezone import now
from rest_framework import serializers
from .models import Competition
from applicant_info.models import ApplicantInfo
from matchtype.serializers import MatchTypeSerializer
from image_url.serializers import ImageUrlSerializer



''' 대회 부분 '''

class CompetitionListSerializer(serializers.ModelSerializer):
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    image_url = serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    can_apply = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'end_date', 'match_type_details', 'tier', 'location', 'image_url', 'status', 'can_apply']
        
    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None

    def get_tier(self, obj):
        if obj.tier:
            return obj.tier.name
        return None
    
    def get_status(self, obj):
        user = self.context['request'].user
        current_applicants_count = obj.applicants.count()
        is_waiting = current_applicants_count >= obj.max_participants
        
        if obj.status == 'before' and not user.is_authenticated or user.gender != obj.match_type.gender or user.tier != obj.tier:
            return '신청 불가능'
        elif obj.status == 'before' and user.is_authenticated and current_applicants_count >= obj.max_participants:
            return '대기 가능'
        elif obj.status == 'before' and user.is_authenticated:
            return '신청 가능'
        elif obj.status == 'during':
            return '대회 진행중'
        else:
            return '대회 종료'


class CompetitionSerializer(serializers.ModelSerializer):
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    image_url = serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    can_apply = serializers.SerializerMethodField()
    is_waiting = serializers.SerializerMethodField()
    waiting_count = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'end_date', 'tier', 'round', 'description', 'rule',
                  'address', 'location', 'code', 'phone', 'fee', 'bank_name',
                  'bank_account_number', 'bank_account_name', 'site_link', 'feedback',
                  'image_url', 'match_type_details', 'status', 'can_apply', 'is_waiting', 'waiting_count']
    
    
    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None
    
    def get_tier(self, obj):
        if obj.tier:
            return obj.tier.name
        return None
    
    def get_status(self, obj):
        if obj.start_date > now():
            return '대회 전'
        elif obj.start_date <= now()  <= obj.end_date:
            return '대회 진행중'
        else:
            return '대회 종료'
        
    def get_can_apply(self, obj):
        user = self.context['request'].user
        # 사용자 인증 확인
        if not user.is_authenticated:
            return False
        
        if user.gender != obj.match_type.gender or user.tier != obj.tier:
            return False
        return True
    
    def get_is_waiting(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            applicant_info = ApplicantInfo.objects.filter(user=user, Competition=obj)