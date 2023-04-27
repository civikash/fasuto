from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from adminc.models import Role, TaskerManager, ReviewCountdown, CustomUser, ClientStuff, SpaceList, ReviewsEmployee, ReviewStatus, TypeReview, Pools
from employee.models import TableEmpl
from login.models import Projectors


#Регистрация моделей в дефолтной админке
admin.site.register(Projectors)
admin.site.register(TaskerManager)
admin.site.register(CustomUser)
admin.site.register(ReviewCountdown)
admin.site.register(Role)
admin.site.register(TableEmpl)
admin.site.register(ReviewStatus)
admin.site.register(ReviewsEmployee)
admin.site.register(TypeReview)
admin.site.register(SpaceList)
admin.site.register(ClientStuff)
admin.site.register(Pools)

