from django.urls import path
from .views import CompetitionApplyAPIView, CompetitionDetailAPIView

urlpatterns = [
    path('competitions/', CompetitionDetailAPIView.as_view(), name='competitions'),
    path('competitions/<int:pk>/', CompetitionDetailAPIView.as_view(), name='competition'),
    path('competitions/<int:pk>/apply/', CompetitionApplyAPIView.as_view(), name='competition-apply'),
]