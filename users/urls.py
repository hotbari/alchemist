from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .views import CreateUserView, LoginView, RefreshAccessTokenView, LogoutView, UserDetailView


urlpatterns = [
    path('auth/token/refresh/', RefreshAccessTokenView.as_view(), name='token_refresh'), # 토큰 리프레시
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # 토큰 검증 # 리프레시토큰 갱신 api
    path('auth/signup/', CreateUserView.as_view(), name='signup'), # 회원가입 api
    path('auth/signin/', LoginView.as_view(), name='login'), # 로그인 api
    path('auth/logout/', LogoutView.as_view(), name='logout'),
     path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
