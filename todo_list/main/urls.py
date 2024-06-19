from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='main'),
    path('users/', include('users.urls')),
    path('accounts/', include('personal_area.urls')),
]