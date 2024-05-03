from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserCreateSerializer, CustomTokenObtainPairSerializer

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
                'accessToken': validated_data.get('access'),  # 액세스 토큰 추가
                'refreshToken': validated_data.get('refresh'),  # 리프레시 토큰 추가
                # 'user': validated_data.get('user'),  # 사용자 정보 조회 (user_id, username, phone 등등..)
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({
                'code': 400,
               'message': '로그인 정보가 올바르지 않습니다.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)