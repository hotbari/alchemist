from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserCreateSerializer, CustomTokenObtainPairSerializer
from django.http import JsonResponse

class CreateUserView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'code': 201,
                'message': '회원가입이 완료 되었습니다',
                'accessToken': str(refresh.access_token),
                'refreshToken': str(refresh),
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            'code': 400,
            'message': '입력값을 확인해주세요',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)

        if serializer.is_valid():
            # 인증이 유효할 경우 serializer에서 반환된 데이터 사용
            validated_data = serializer.validated_data

            # 응답 데이터 구조 정의
            response_data = {
                'message': '정상적으로 로그인 완료',
                'accessToken': validated_data.get('access'),  # 액세스 토큰 추가
                'refreshToken': validated_data.get('refresh'), 
                # 'user': validated_data.get('user'),  # 사용자 정보 조회 (user_id, username, phone 등등..)
            }
            

            # JsonResponse로 응답 생성
            response = JsonResponse(response_data, status=status.HTTP_200_OK)
            # refresh token 쿠키에 저장
            response.set_cookie(
                'refresh_token',
                validated_data.get('refresh'),
                httponly=True,  # JavaScript를 통한 접근 방지 (XSS 해킹 방지?)
                max_age=30 * 24 * 60 * 60,  # 현재값 30일 -  쿠키 유효 기간 (24 * 60 * 60  = 86400초, 즉 1일)
            )
            return response
        
        else:
            return Response({
                'code': 400,
               'message': '로그인 정보가 올바르지 않습니다.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
                
       