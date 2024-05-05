from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status



# 회원가입 ##

from .serializers import UserSerializer, CustomTokenObtainPairSerializer

class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = CustomTokenObtainPairSerializer.get_token(user)
            response = Response({
                'message': '회원가입이 완료 되었습니다',
            }, status=status.HTTP_201_CREATED)
            
            response.set_cookie('access',value=str(token.access_token), httponly= True)
            response.set_cookie('refresh',value=str(token), httponly= True)
            
            return response

        return Response({
            'code': 400,
            'message': '입력값을 확인해주세요',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



# 로그인 ##

from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        res = super().post(request, *args, **kwargs)
        
        response = Response({
            "detail": "로그인 되었습니다."
            }, status= status.HTTP_200_OK)
        
        response.set_cookie("refresh", res.data.get('refresh', None), httponly= True)
        response.set_cookie("access", res.data.get('access', None), httponly= True)

        return response     
    
    
    
## 로그아웃 ##
from rest_framework import status
from django.http import JsonResponse

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = JsonResponse({
            'detail': '로그아웃되었습니다'
            }, status=status.HTTP_200_OK)
        
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        
        return response
