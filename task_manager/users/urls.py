from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='users'),
    path('<int:id>/update/', views.UpdateView.as_view(), name='user_update'),
    path('<int:id>/delete/', views.IndexView.as_view(), name='user_delete'),
    path('create/', views.CreateView.as_view(), name='user_create')
]