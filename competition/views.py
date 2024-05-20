from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from datetime import timedelta
from django.utils.timezone import now

from .models import Competition
from users.models import CustomUser
from matchtype.models import MatchType
from applicant_info.models import ApplicantInfo
from applicant.models import Applicant
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
            return Response({'error': '대회를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)



# """ """
class CompetitionApplyView(APIView):
    def post(self, request, pk):
        
        try: # 대회 조회
            competition = Competition.objects.get(pk=pk)
        except Competition.DoesNotExist:
            return Response({'error': '대회를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # 코드 확인
        submitted_code = request.data.get('code')
        if submitted_code != competition.code:
            return Response({'error': '제출된 코드가 유효하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 로그인 확인
        applicant = request.user # 신청자 = 로그인한 유저
        if not applicant.is_authenticated: # 유저 검증
            return Response({'error': '로그인되어 있지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        partner_id = request.data.get('partner_id')  #신청 폼에서 제공된 파트너의 ID
        partner = CustomUser.objects.get(id=partner_id) # 파트너 인스턴스 생성
        
        # 자기 자신 선택 불가
        if applicant.id == partner_id:
            return Response({'error': '신청자를 파트너로 선택할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        #신청자 중복 신청 확인
        # if Applicant.objects.filter(applicant_info__competition=competition, user=applicant).exists():
        #     return Response({'error': '해당 대회에 이미 신청하셨습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # # 파트너 중복 신청 확인
        # elif partner_id and Applicant.objects.filter(applicant_info__competition=competition, user_id=partner_id).exists():
        #     return Response({'error': '선택하신 파트너는 이미 해당 대회를 신청하셨습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 혼성 확인
        if competition.match_type.gender == 'mix' and applicant.gender == partner.gender:
            return Response({'error': '혼성 경기는 서로 다른 성별의 파트너가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 복식 신청
        if competition.match_type.type == 'duo':
            try:
                partner = CustomUser.objects.get(id=partner_id)
            except CustomUser.DoesNotExist:
                return Response({'error': '파트너를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # 단식 신청
        return self.handle_singles(request, competition, applicant)
        
    
    def handle_singles(self, request, competition, applicant):
        # 단식 신청 처리 로직
        current_applicants_count = ApplicantInfo.objects.filter(competition=competition).count()
        is_waiting = current_applicants_count >= competition.max_participants
        application_status = '대기 신청' if is_waiting else '대회 신청'
        
        applicant_info_data = {
                    'competition': competition.id,
                    'is_waiting': is_waiting,
                    'expired_date': now() + timedelta(days=competition.deposit_date)
            }
        
        serializer = ApplicantInfoSerializer(data=applicant_info_data)
        if serializer.is_valid():
            applicant_info = serializer.save() 
        else:
                return Response(ApplicantInfoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        applicant_data = {'user': applicant.id, 'applicant_info': applicant_info.id}
        applicant_serializer = ApplicantSerializer(data=applicant_data)
        if applicant_serializer.is_valid():
            applicant_serializer.save()
            return Response({'message': '단식 경기 신청 완료.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(applicant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def handle_doubles(self, request, competition, applicant, partner):
        # 복식 신청 처리 로직
        with transaction.atomic(): # 2개 신청 동시 처리
            
            # 해당 대회 신청된 참가정보 확인 후 대기여부 판별
            current_applicants_count = ApplicantInfo.objects.filter(competition=competition).count()
            is_waiting = current_applicants_count >= competition.max_participants
            
            applicant_info_data = {
                    'competition': competition.id,
                    'is_waiting': is_waiting,
                    'expired_date': now() + timedelta(days=competition.deposit_date)
            }
            serializer = ApplicantInfoSerializer(data=applicant_info_data)
            if serializer.is_valid():
                applicant_info = serializer.save()
            else:
                return Response(ApplicantInfoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            for user in [applicant, partner]:
                applicant_data = {'user': user.id, 'applicant_info': applicant_info.id}
                applicant_serializer = ApplicantSerializer(data=applicant_data)
                if not applicant_serializer.is_valid():
                    return Response(applicant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                applicant_serializer.save()
                response_data = applicant_serializer.data
                response_data.update({
                    'application_amount': f"{current_applicants_count+1}팀",
                    'payment_info': {  # 결제 정보 추가
                        'bank_name': competition.bank_name,
                        'bank_account_number': competition.bank_account_number,
                        'bank_account_name': competition.bank_account_name,
                        'fee': competition.fee
                    }
                })
        return Response(response_data, status=status.HTTP_201_CREATED)