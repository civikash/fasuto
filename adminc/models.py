from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from employee.models import TableEmpl
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


#Модель для определения ролей в системе
class Role(models.Model):
    ADMIN = 'Администратор'
    SPECTATOR = 'Наблюдатель'
    EMPLOYEE = 'Работник'

    ROLE_CHOICES = [
        (ADMIN, _('Администратор')),
        (SPECTATOR, _('Наблюдатель')),
        (EMPLOYEE, _('Работник'))
    ]
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, default=ADMIN)

    
    def __str__(self):
        return self.name

class Pools(models.Model):
    FULL = 'Общие отзывы'
    ONLY_POSTITIVE = 'Положительные'
    ONLY_NEGATIVE = 'Отрицательные'

    POOLS_CHOICES = [
        (FULL, _('Общие отзывы')),
        (ONLY_POSTITIVE, _('Положительные')),
        (ONLY_NEGATIVE, _('Отрицательные'))
    ]
    name = models.CharField(max_length=50, choices=POOLS_CHOICES)

    
    def __str__(self):
        return self.name

#Дополнение к главной модели User в Django, в дальнейшем надо уазывать на нее. Используя AbstractUser мы может добавлять новые поля не изменяя основной контур
class CustomUser(AbstractUser):
    pool = models.ForeignKey(Pools, on_delete=models.CASCADE, related_name='custom_pools', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='custom_users', null=True, blank=True)


#Таблица для записи действий пользотваелей
class UserAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class TypeReview(models.Model):
    NULL='Не выбран'
    POSITIVE = 'Позитивный'
    NEGATIVE = 'Отрицательный'

    POSNEG_CHOICES = [
        (POSITIVE, _('Позитивный')),
        (NEGATIVE, _('Отрицательный'))
    ]
    name = models.CharField(max_length=50, choices=POSNEG_CHOICES, default=NULL)

    def __str__(self):
        return self.name

class ReviewStatus(models.Model):
    NULL = 'Отзыв не проверен'
    ACCEPT = 'Отзыв проверен'
    MODERATION = 'На модерации'
    NO_UNIQUE = 'Отзыв не уникален'

    STATUS_CHOICES = [
        (NULL, _('Отзыв не проверен')),
        (ACCEPT, _('Отзыв проверен')),
        (MODERATION, _('На модерации')),
        (NO_UNIQUE, _('Отзыв не уникален'))
    ]
    name = models.CharField(max_length=50, choices=STATUS_CHOICES, default=NULL)

    def __str__(self):
        return self.name

class ClientStuff(models.Model):
    NULL = 'Ничего'
    CLIENT = 'Клиент'
    STUFF = 'Сотрудник'

    CLIENT_CHOICES = [
        (CLIENT, _('Клиент')),
        (STUFF, _('Сотрудник'))
    ]
    name = models.CharField(max_length=50, choices=CLIENT_CHOICES, default=NULL)

    def __str__(self):
        return self.name


class SpaceList(models.Model):
    name = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.name

class ReviewsEmployee(models.Model):
    CHECKING = 'На проверке'
    GOOD = 'Одобрен'
    NULL = 'Нет статуса'

    STATUS_CHOICES = [
        (CHECKING, _('На проверке')),
        (GOOD, _('Одобрен')),
        (NULL, _('Нет статуса'))
    ]
    owner = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    type_stuff = models.ForeignKey(ClientStuff, on_delete=models.PROTECT)
    re_login = models.CharField(max_length=35, null=False)
    re_password = models.CharField(max_length=35, null=False)
    re_firstname = models.CharField(max_length=35, null=False)
    re_lastname = models.CharField(max_length=35, null=False)
    space = models.ForeignKey(SpaceList, on_delete=models.CASCADE)
    office = models.CharField(max_length=300, null=False)
    check_review = models.CharField(max_length=100, choices=STATUS_CHOICES, default=CHECKING)
    global_check_review = models.CharField(max_length=100, choices=STATUS_CHOICES, default=NULL)
    review_text = models.TextField()
    note = models.CharField(max_length=150, null=True)
    type_review = models.ForeignKey(TypeReview, on_delete=models.CASCADE)
    status = models.ForeignKey(ReviewStatus, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)


class TaskerManager(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    text = models.CharField(max_length=250, null=False)
    global_task = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review Countdown {self.text}"

class ReviewCountdown(models.Model):
    review = models.OneToOneField(ReviewsEmployee, on_delete=models.CASCADE, related_name='countdown')
    days_left = models.IntegerField()
    start_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review Countdown {self.review.id}"


#Сигнал для автоматичнского создания объектов в модели (таблице) роли
@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if Role.objects.exists():
        return
    Role.objects.create(name='Администратор')
    Role.objects.create(name='Наблюдатель')
    Role.objects.create(name='Работник')

#Присвоение роли при создании суперпользователя
@receiver(post_save, sender=CustomUser)
def create_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        instance.role = instance.role or Role.objects.get(name='Администратор')
        instance.save()
