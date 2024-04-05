from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.UsersIndexView.as_view(), name='users'),
    path('<int:id>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:id>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('create/', views.UserCreateView.as_view(), name='user_create')
]