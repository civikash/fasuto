from django.contrib import admin
from django.urls import path
from login.views import LoginView, LogoutView, chart_projectors

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('kwork/', chart_projectors, name='kwork')
]