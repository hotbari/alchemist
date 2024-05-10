from django.urls import path
from .views import (ClubListView,
                    ClubDetailView
)

urlpatterns = [
    path('club/list/', ClubListView.as_view(), name='club-list'), # 클럽 목록 조회 API
    path('club/<int:pk>/', ClubDetailView.as_view(), name='club-detail'), # 클럽 상세 정보 API
]
