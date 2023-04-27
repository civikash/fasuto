from .models import Role
from adminc.models import CustomUser


#Создается глобальный def который можно использовать в любом шаблоне. Здесь осуществляется проверка роли пользователя в системе.
#Можно использовать контекст user_role в шаблоне чтобы ограничивать доступ
def role_context(request):
    role_name = None
    if request.user.is_authenticated:
        try:
            role_name = request.user.role.custom_users.first().role.name
        except CustomUser.DoesNotExist:
            pass
    return {'user_role': role_name}