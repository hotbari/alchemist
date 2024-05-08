from django.contrib import admin
from django.urls import path, include  # include 함수를 임포트합니다.
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from users.views import CreateUserView, LoginView, LogoutView, RefreshAccessTokenView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')), # include를 활용하여 각 독립적인app의 urls.py 를 포함 시킴
    path('api/v1/', include('club.urls')),
]
