from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CreateUserView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls), # 장고 admin page 경로
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # 리프레시토큰 갱신 api
    path('auth/signup/', CreateUserView.as_view(), name='signup'), # 회원가입 api
    path('auth/signin/', LoginView.as_view(), name='login'), # 로그인 api
]
