from django.urls import path
from . import views

urlpatterns = [
    path('create-team/', views.TeamCreateView.as_view(), name='create_team'),
    path('list-team/', views.TeamListView.as_view(), name='list_teams'),
    path('describe-team/', views.TeamDescribeView.as_view(), name='describe_team'),
    path('update-team/', views.TeamUpdateView.as_view(), name='update_team'),
    path('add-users-team/', views.TeamAddUsersView.as_view(), name='add_users_to_team'),
    path('remove-users-team/', views.TeamRemoveUsersView.as_view(), name='remove_users_from_team'),
    path('team-users/', views.TeamUsersView.as_view(), name='list_team_users'),
]