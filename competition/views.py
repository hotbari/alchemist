from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from datetime import timedelta

from .models import Competition
from users.models import CustomUser
from matchtype.models import MatchType
from applicant_info.models import ApplicantInfo
from .serializers import CompetitionListSerializer, CompetitionSerializer
from applicant_info.serializers import ApplicantInfoSerializer
from applicant.serializers import ApplicantSerializer


class CompetitionListView(APIView):
    """
    대회 리스트
    """
    def get(self, request):
        # 쿼리 파라미터로부터 gender와 type을 받아옵니다.
        gender = request.query_params.get('gender')
        type = request.query_params.get('match_type')

        if gender and type:
            competitions = Competition.objects.filter(match_type__gender=gender, match_type__type=type)
        else:
            competitions = Competition.objects.all()

        serializer = CompetitionListSerializer(competitions, many=True)
        return Response(serializer.data)
    

class CompetitionView(APIView):
    """
    대회 상세보기
    """
    def get(self, request, pk):
        try:
            competition = Competition.objects.get(pk=pk)
            serializer = CompetitionSerializer(competition)
            return Response(serializer.data)
        except Competition.DoesNotExist:
            return Response({'error': 'competition not found'}, status=status.HTTP_404_NOT_FOUND)



# """ """
class CompetitionApplyView(APIView):
    def post(self, request, pk):
        try:
            competition = Competition.objects.get(pk=pk)
        except Competition.DoesNotExist:
            return Response({'error': 'Competition not found'}, status=status.HTTP_404_NOT_FOUND)
        
        submitted_code = request.data.get('code')
        if submitted_code != competition.code:
            return Response({'error': '제출된 코드가 유효하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        applicant = request.user # 현재 로그인한 사용자를 신청자로 설정
        partner_id = request.data.get('partner_id') #신청 폼에서 제공된 파트너의 ID
        # 파트너 처리 로직
        if competition.match_type.type == 'duo' and partner_id:
            try:
                partner = CustomUser.objects.get(id=partner_id)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Invalid partner ID'}, status=status.HTTP_404_NOT_FOUND)
            return self.handle_doubles(competition, applicant, partner)
        
        
        current_applicants_count = ApplicantInfo.objects.filter(competition=competition).count()
        is_waiting = current_applicants_count >= competition.max_participants
        
        data = {
            'competition': competition.id,
            'user': applicant.id,
            'is_waiting': is_waiting,
            'expired_date': competition.created_at + timedelta(days=3)  # Set expired date
        }

        serializer = ApplicantInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response_data.update({
                'payment_info': {
                    'bank_name': competition.bank_name,
                    'bank_account_number': competition.bank_account_number,
                    'bank_account_name': competition.bank_account_name,
                    'fee': competition.fee
                },
                'is_waiting': is_waiting
            })
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def handle_doubles(self, competition, applicant, partner):
        with transaction.atomic():
            current_applicants_count = ApplicantInfo.objects.filter(competition=competition).count()
            is_waiting = current_applicants_count >= competition.max_participants
            
            applicant_info_date = {
                    'competition': competition.id,
                    'is_waiting': is_waiting,
                    'expired_date': competition.created_at + timedelta(days=competition.deposit_date)
            }
            applicant_info_serializer = ApplicantInfoSerializer(data=applicant_info_date)
            if applicant_info_serializer.is_valid():
                applicant_info = applicant_info_serializer.save()
            else:
                return Response(applicant_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
            for user in [applicant, partner]:
                applicant_data = {'user': user.id, 'applicant_info': applicant_info.id}
                applicant_serializer = ApplicantSerializer(data=applicant_data)
                if not applicant_serializer.is_valid():
                    transaction.set_rollback(True)
                    return Response(applicant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                applicant_serializer.save()

        return Response({'message': '복식 경기 신청 완료.', 'applicant_info': applicant_info_serializer.data}, status=status.HTTP_201_CREATED)