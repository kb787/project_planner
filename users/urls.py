from django.urls import path
from project_planner.users import views

urlpatterns = [
    path('create-user/', views.UserCreateView.as_view(), name='create_user'),
    path('list-user/', views.UserListView.as_view(), name='list_users'),
    path('describe-user/', views.UserDescribeView.as_view(), name='describe_user'),
    path('update-user/', views.UserUpdateView.as_view(), name='update_user'),
    path('user-teams/', views.UserTeamsView.as_view(), name='user_teams'),
]