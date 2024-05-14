from django.urls import path
from .views import CompetitionListView, CompetitionView
# CompetitionApplyAPIView 

urlpatterns = [
    path('competitions/', CompetitionListView.as_view(), name='competitions'),
    path('competitions/<int:pk>/', CompetitionView.as_view(), name='competition'),
    # path('competitions/<int:pk>/apply/', CompetitionApplyAPIView.as_view(), name='competition-apply'),
]