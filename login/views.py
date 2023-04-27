from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import View
from django.shortcuts import render
from .models import Projectors
from django.db.models import Count, Q
import json
from django.views.generic import TemplateView, ListView
#from qsstats import QuerySetStats
#from itertools import chain
# Create your views here.


#Представление для авторизации на сайте
class LoginView(View):
    template_name = 'login/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('global_panel')
        else:
            error_message = 'Неверные имя пользователя или пароль'
            return render(request, self.template_name, {'error_message': error_message})

#Представление для выхода
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    

def index(request):
    table_projectors = Projectors.objects.all()


    return render(request, 'login/index.html', {'table_projectors': table_projectors})

def chart_projectors(request):
    # Получаем список всех проекторов
    projectors = Projectors.objects.all()

    # Создаем словарь, в котором будем хранить информацию о датах обслуживания и ремонта каждого проектора
    data_by_projector = {}

    # Для каждого проектора получаем информацию о датах обслуживания и ремонта
    for projector in projectors:
        name = projector.model
        service_date = projector.date_service
        repair_date = projector.date_repair

        # Если дата обслуживания или ремонта есть, то добавляем ее в словарь data_by_projector
        if service_date or repair_date:
            if name in data_by_projector:
                data_by_projector[name]['service_dates'].append(service_date)
                data_by_projector[name]['repair_dates'].append(repair_date)
            else:
                data_by_projector[name] = {'service_dates': [service_date], 'repair_dates': [repair_date]}

    # Создаем списки с датами обслуживания и ремонта для каждого проектора
    service_data = []
    repair_data = []

    for name, data in data_by_projector.items():
        service_dates = [d.strftime('%Y-%m-%d') for d in data['service_dates'] if d]
        repair_dates = [d.strftime('%Y-%m-%d') for d in data['repair_dates'] if d]

        service_data.append({'name': name, 'data': service_dates})
        repair_data.append({'name': name, 'data': repair_dates})

    # Создаем контекст и передаем его в шаблон
    context = {
        'service_data': service_data,
        'repair_data': repair_data,
    }
    return render(request, 'login/diagram.html', context)




def about(request):
    return render(request, 'mainapp/about.html')

def diagram(request):
    return render(request, 'mainapp/diagram.html')

