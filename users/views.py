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
                'access': str(token.access_token)
            }, status=status.HTTP_201_CREATED)
            
            
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
            "message": "확인되었습니다.",
            "access": str(res.data.get('access', None))
            }, status= status.HTTP_200_OK)
        
        response.set_cookie("refresh", res.data.get('refresh', None), httponly= True)
        # response.set_cookie("access", res.data.get('access', None), httponly= True)

        return response     
    
    
    
## 로그아웃 ##
from rest_framework import status
from django.http import JsonResponse

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = JsonResponse({
            'detail': '로그아웃되었습니다'
            }, status=status.HTTP_200_OK)
        
        response.delete_cookie('refresh')
        
        return response



## 액세스 토큰 리프레시 ##

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class RefreshAccessTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token is None:
            return Response({"error": "리프레시 토큰이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)

            # 필요하다면 새 리프레시 토큰도 생성하여 반환할 수 있습니다. 
            # new_refresh_token = str(token)

            response = Response()
            response.data = {
                'access': new_access_token,
                # 'refresh': new_refresh_token,
            }

            return response
        except Exception as e:
            return Response({"error": "인증되지 않은 리프레시 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)