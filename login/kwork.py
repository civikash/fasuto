from django.shortcuts import render
from .models import Projectors, PrintersMFP, CPU, HDD, Motherboard, RAM, OpticalDrive, VideoCard, PersonalComputer
from .models import Software, Service
from django.db.models import Count, Q
import json
from django.views.generic import TemplateView, ListView
#from qsstats import QuerySetStats
#from itertools import chain
# Create your views here.

def index(request):
    table_projectors = Projectors.objects.all()
    table_printersmfp = PrintersMFP.objects.all()
    table_cpu = CPU.objects.all()
    table_hdd = HDD.objects.all()
    table_motherboard = Motherboard.objects.all()
    table_ram = RAM.objects.all()
    table_optical_drive = OpticalDrive.objects.all()
    table_video_card = VideoCard.objects.all()
    table_personal_computers = PersonalComputer.objects.all()
    table_software = Software.objects.all()
    table_service = Service.objects.all()

    return render(request, 'mainapp/index.html', {'table_projectors': table_projectors,
                                                  'table_printersmfp': table_printersmfp,
                                                  'table_cpu': table_cpu,
                                                  'table_hdd': table_hdd,
                                                  'table_motherboard': table_motherboard,
                                                  'table_ram': table_ram,
                                                  'table_optical_drive': table_optical_drive,
                                                  'table_video_card': table_video_card,
                                                  'table_personal_computers': table_personal_computers,
                                                  'table_software': table_software,
                                                  'table_service': table_service})

def chart_projectors(request):
    projectors = Projectors.objects.all()

    # Получаем количество проекторов с определенным типом обслуживания
    serviced = Projectors.objects.filter(date_service__isnull=False).count()
    repaired = Projectors.objects.filter(date_repair__isnull=False).count()

    # Формируем данные для графика
    chart_categories = ['Техническое обслуживание', 'Ремонт']
    chart_data = [serviced, repaired]

    context = {
        'projectors': projectors,
        'chart_categories': chart_categories,
        'chart_data': chart_data,
    }
    return render(request, 'mainapp/diagram.html', context)




def about(request):
    return render(request, 'mainapp/about.html')

def diagram(request):
    return render(request, 'mainapp/diagram.html')

