from django.contrib import admin
from django.urls import path, include  # include 함수를 임포트합니다.
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from users.views import CreateUserView, LoginView, LogoutView, RefreshAccessTokenView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/signup/', CreateUserView.as_view(), name='signup'),  # 회원가입
    path('api/v1/auth/signin/', LoginView.as_view(), name='login'),  # 로그인
    path('api/v1/auth/logout/', LogoutView.as_view(), name='logout'),  # 로그아웃
    path('api/v1/auth/token/refresh/', RefreshAccessTokenView.as_view(), name='token_refresh'), # 토큰 리프레시
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # 토큰 검증
    path('api/v1/', include('users.urls')), # include를 활용하여 각 독립적인app의 urls.py 를 포함 시킴
    path('api/v1/', include('club.urls')),
]
