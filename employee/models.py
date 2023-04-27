from django.db import models
from django.conf import settings


#Обычная таблица
class TableEmpl(models.Model):
    number = models.CharField(max_length=15, null=False)
    description = models.CharField(max_length=115)
    title = models.CharField(max_length=75, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #Если вы захотите использовать ключи на юзера то используйте settings.AUTH_USER_MODEL