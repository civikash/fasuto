from django.contrib import admin
from django.urls import path
from adminc.views.views import GlobalPanel, CreateUser, DeleteUser

urlpatterns = [
    path('admin_panel/', GlobalPanel.as_view(), name='global_panel'),
    path('create_user/', CreateUser.as_view(), name='create_user'),
    #URL на удаление пользовтаеля, обратите внимание на констуркцию int:user_id
    path('delete_user/<int:user_id>/', DeleteUser.as_view(), name='delete_user'),
]