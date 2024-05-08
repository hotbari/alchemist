from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CreateUserSerializer, CustomTokenObtainPairSerializer



# 회원가입 view ##


class CreateUserView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # 멀티파트 데이터를 처리할 수 있도록 파서 클래스 추가

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)  # request.data를 직접 사용
        
        if serializer.is_valid():
            user = serializer.save()
            token = CustomTokenObtainPairSerializer.get_token(user)  # 사용자를 위한 토큰 생성
            response = Response({
                'message': '회원가입이 완료 되었습니다',
            }, status=status.HTTP_201_CREATED)
            
            # 생성된 토큰을 쿠키에 설정
            response.set_cookie('access', value=str(token.access_token), httponly=True)
            response.set_cookie('refresh', value=str(token), httponly=True)
            
            return response

        return Response({
            'code': 400,
            'message': '입력값을 확인해주세요',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



# 로그인 ##


class LoginView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        res = super().post(request, *args, **kwargs)
        
        response = Response({
            "message": "로그인 되었습니다."
            }, status= status.HTTP_200_OK)
        
        response.set_cookie("refresh", res.data.get('refresh', None), httponly= True)
        response.set_cookie("access", res.data.get('access', None), httponly= True)

        return response     
    
    
    
## 로그아웃 ##
from django.http import JsonResponse

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = JsonResponse({
            'detail': '로그아웃되었습니다'
            }, status=status.HTTP_200_OK)
        
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        
        return response