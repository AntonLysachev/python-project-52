from django.urls import path
from task_manager.labels import views


urlpatterns = [
    path('', views.LabelsIndexView.as_view(), name='labels'),
    path('<int:id>/update/', views.LabelUpdateView.as_view(), name='label_update'),
    path('<int:id>/delete/', views.LabelDeleteView.as_view(), name='label_delete'),
    path('create/', views.LabelCreateView.as_view(), name='label_create')
]