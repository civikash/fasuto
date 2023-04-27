from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-custom/', include('adminc.urls')),
    path('', include('login.urls')),
    path('', include('employee.urls'))
]
