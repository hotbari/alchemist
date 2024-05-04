from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserSerializer


## 회원가입 ##

class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
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



## 로그인 ##

from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(TokenObtainPairView):
    # TokenObtainPairView 의 response 는 refresh, access 토큰 정보를 반환하기 때문에
    # "로그인 되었습니다." 로 바꾸고 토큰은 쿠키에 담아서 응답.
    def post(self, request: Request, *args, **kwargs) -> Response:
        res = super().post(request, *args, **kwargs)
        
        response = Response({
            "detail": "로그인 되었습니다.",
            'accessToken':  res.data.get('access'),
            'refreshToken':  res.data.get('refresh'),
            }, status= status.HTTP_200_OK)
        
        response.set_cookie("refresh", res.data.get('refresh', None), httponly= True)
        response.set_cookie("access", res.data.get('access', None), httponly= True)

        return response     
    
    
    
## 로그아웃 ##
  
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "로그아웃 되었습니다."})
