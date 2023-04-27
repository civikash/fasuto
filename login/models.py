from django.db import models


class Projectors(models.Model):
    pk_Projectors = models.AutoField(primary_key='True', verbose_name='ПК_Проектора')
    inventory_number = models.PositiveIntegerField(verbose_name='Инвент. номер')
    model = models.CharField(verbose_name='Модель', max_length=50)
    date_service = models.DateField(verbose_name='Дата обслуживания', null=True, blank=True)
    date_repair = models.DateField(verbose_name='Дата ремонта', null=True, blank=True)
    malfunctions = models.TextField(verbose_name='Неисправности', null=True, blank=True)
    location = models.CharField(verbose_name='Месторасположение', max_length=25)
    other = models.CharField(verbose_name='Прочее', max_length=250, null=True, blank=True)

    def __str__(self):
        return f'Проектор: {self.model + "   " + self.location}'

    class Meta:
        verbose_name = 'Проектор'
        verbose_name_plural = 'Проекторы'