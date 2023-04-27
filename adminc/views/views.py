from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from adminc.models import Role, TaskerManager, CustomUser, UserAction, ReviewsEmployee, Pools
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.models import TableEmpl
from django.db.models import Count
import json


class GlobalPanel(LoginRequiredMixin, View):
    #Если пользователь не авторизован, буде редирект на страницу авторизации
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    #Сам шаблон
    template_name = 'adminc/global_panel.html'

    #Метод get  в данном случае просто отображает шаблон
    def get(self, request, *args, **kwargs):
        actions = UserAction.objects.all()
        task_list = TaskerManager.objects.filter(owner=request.user)
        reviews_count = ReviewsEmployee.objects.values('owner__username').annotate(count=Count('owner__username')).order_by('-count')
        reviews = ReviewsEmployee.objects.all().count()
        context = {'actions': actions, 'task_list': task_list, 'reviews': reviews, 'reviews_count': reviews_count}
        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        date = request.POST.get('date_task')
        text = request.POST.get('text_task')
        true = request.POST.get('global_task')

        if true:
            true = True
        new_record = TaskerManager(owner=request.user, text=text, start_date=date, global_task = true )
        new_record.save()

        return HttpResponseRedirect(request.path_info)
    
    

class CreateUser(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'adminc/create_user.html'

    def get(self, request, *args, **kwargs):
        pools = Pools.objects.all()
        #Получаем все роли
        roles = Role.objects.all()
        #Получаем всех пользователей
        users = CustomUser.objects.all()
        #Передаем в контекст и выводим в шаблон
        context= {'roles': roles, 'users': users, 'pools': pools}
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        #Получаем значения из name input в шаблоне и записываем в переменные
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        role_id = request.POST.get('role')
        pool_id = request.POST.get('pool')

        #Если наблюдатель был создан то ошибка
        if role_id == '2':
            if CustomUser.objects.filter(role_id=2).exists():
                return HttpResponseBadRequest("Может быть лишь один Наблюдатель")

        #Получаем выбранную роль и сохраянем нового пользователя
        role = Role.objects.get(id=role_id)
        pool = Pools.objects.get(id=pool_id)
        user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, role=role, pool=pool)
        return HttpResponseRedirect(request.path_info)
    
class DeleteUser(View):
    template_name = 'users/delete_user.html'

    def get(self, request, user_id, *args, **kwargs):
        #Получаем id пользователя который был определен в urls (в get передается user_id из url)
        user = CustomUser.objects.get(id=user_id)
        context= {'user': user}
        return render(request, self.template_name, context=context)
    
    def post(self, request, user_id):
        #Получаем POST запрос и удаляем пользователя
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return redirect(reverse('create_user'))