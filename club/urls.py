from django.urls import path
from .views import ClubListView

urlpatterns = [
    path('club/list/', ClubListView.as_view(), name='club-list'),  # 클럽 목록 조회 API
]
