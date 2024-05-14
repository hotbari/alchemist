from django.urls import path
from .views import TeamDetailView, TeamUsersListView


urlpatterns = [# 클럽 목록 조회 API
    path('team/<int:pk>/', TeamDetailView.as_view(), name='team-detail'), # 팀 상세 정보 API
    path('team/<int:pk>/userlist/', TeamUsersListView.as_view(), name='team-users-list'), # 팀에 속한 유저 전체 목록 조회 API
]