from django.urls import path
from . import views

urlpatterns = [
    path('create-board/', views.BoardCreateView.as_view(), name='create_board'),
    path('close-board/', views.BoardCloseView.as_view(), name='close_board'),
    path('task/add/', views.TaskAddView.as_view(), name='add_task'),
    path('task/update-status/', views.TaskUpdateStatusView.as_view(), name='update_task_status'),
    path('list-board/', views.BoardListView.as_view(), name='list_boards'),
    path('export-board/', views.BoardExportView.as_view(), name='export_board'),
]