from django.urls import path
from .views import TeamDetailView


urlpatterns = [# 클럽 목록 조회 API
    path('team/<int:pk>/', TeamDetailView.as_view(), name='team-detail'), # 팀 상세 정보 API
]