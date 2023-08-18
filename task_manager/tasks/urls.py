from django.urls import path

from .views import (TasksFilterView, TaskCreateView,
                    TaskUpdateView, TaskDeleteView,
                    TaskDetailView)

app_name = 'tasks'

urlpatterns = [
    path('', TasksFilterView.as_view(), name='tasks_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
]
