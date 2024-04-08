from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path('', views.StatusesIndexView.as_view(), name='statuses'),
    path('<int:id>/update/', views.StatusUpdateView.as_view(), name='status_update'),
    path('<int:id>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
    path('create/', views.StatusCreateView.as_view(), name='status_create')
]