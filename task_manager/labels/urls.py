from django.urls import path

from .views import (LabelsListView, LabelCreateView,
                    LabelUpdateView, LabelDeleteView)

app_name = 'labels'

urlpatterns = [
    path('', LabelsListView.as_view(), name='labels_list'),
    path('create/', LabelCreateView.as_view(), name='label_create'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='label_update'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='label_delete'),
]
