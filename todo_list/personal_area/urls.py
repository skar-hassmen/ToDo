from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda request: redirect('profile', 'all', 'none')),
    path('profile/', lambda request: redirect('profile', 'all', 'none'), name='profile_main'),
    path('profile/?filter=<str:filter>&sorted=<str:sorted>', views.Account.as_view(), name='profile'),
    path('create_task/', views.CreateTask.as_view(), name='create_task'),
    path('done_task/id=<int:id_task>', views.DoneTask.as_view(), name='done_task'),
    path('delete_task/id=<int:id_task>', views.DeleteTask.as_view(), name='delete_task'),
    path('edit_task/id=<int:pk>', views.EditTask.as_view(), name='edit_task'),
    path('create_task_error/', views.CreateTaskError.as_view(), name='create_task_error'),
    path('edit_task_error/', views.EditTaskError.as_view(), name='edit_task_error'),
    path('login_error/', views.LoginError.as_view(), name='login_error'),
]
