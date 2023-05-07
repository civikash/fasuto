from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView, ListView
from django.contrib.auth.models import User
from adminc.models import Role, CustomUser, TaskerManager, ReviewCountdown, UserAction, ReviewsEmployee, ClientStuff, SpaceList, TypeReview, ReviewStatus
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from employee.models import TableEmpl
from employee.forms import TableEmplForm, ReviewsEmployeeFilterForm, ReviewForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
import os
import traceback
import datetime
import json


class CheckServiceView(View):
    def post(self, request, *args, **kwargs):
        service = request.POST.get('select_space')
        try:
            if service == '1':
                os.system('python ./parsers/2gis.py')
            elif service == '2':
                os.system('python ./parsers/yandex.py')
            elif service == '3':
                os.system('python ./parsers/flamp.py')
            elif service == '4':
                os.system('python ./parsers/zoon.py')
        except Exception as e:
            traceback.print_exc()
            traceback.print_exc(file=open('/var/log/gunicorn/error.log', 'a'))
            traceback.print_exc(file=open('/var/log/gunicorn/tracerback.log', 'a'))
        return redirect('review')
    
class CheckAllServiceView(View):
    def post(self, request, *args, **kwargs):
        os.system('python ./parsers/2gis.py')
        os.system('python ./parsers/yandex.py')
        os.system('python ./parsers/flamp.py')
        os.system('python ./parsers/zoon.py')
        return redirect('review')
    
class CheckOneServiceView(View):
    def post(self, request, *args, **kwargs):
        os.system('python ./parsers/number6.py')
        return redirect('review')

class TableReviewView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = ReviewsEmployee
    redirect_field_name = 'redirect_to'
    template_name = 'employee/table_review.html'

    def post(self, request, *args, **kwargs):
        if 'accept' in request.POST:
            review_id = request.POST.get('accept').split('-')[0]
            review = ReviewsEmployee.objects.get(id=review_id)
            review.check_review = ReviewsEmployee.GOOD
            review.save()
        elif 'reject' in request.POST:
            review_id = request.POST.get('reject').split('-')[0]
            review = ReviewsEmployee.objects.get(id=review_id)
            review.check_review = ReviewsEmployee.REJECT
            review.status = ReviewStatus.objects.get(name=ReviewStatus.NO_UNIQUE)
            review.save()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        owner_name = self.request.GET.get('owner_name')
        created_date = self.request.GET.get('created_date')
        space_name = self.request.GET.get('space_name')
        office_name = self.request.GET.get('office_name')
        status_name = self.request.GET.get('status_name')
        type_review_name = self.request.GET.get('type_review_name')

        if owner_name:
            queryset = queryset.filter(owner__username=owner_name)
        if created_date:
            date = timezone.datetime.strptime(created_date, '%Y-%m-%d').date()
            queryset = queryset.filter(create_date=date)
        if space_name:
            queryset = queryset.filter(space__name=space_name)
        if office_name:
            queryset = queryset.filter(office__icontains=office_name)
        if status_name:
            queryset = queryset.filter(status__name=status_name)
        if type_review_name:
            queryset = queryset.filter(type_review__name=type_review_name)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        context['stuffs'] = ClientStuff.objects.all()
        context['spaces'] = SpaceList.objects.all()
        context['status_type'] = ReviewStatus.objects.all()
        context['re_globals'] = ReviewsEmployee.objects.all()
        context['myreview'] = ReviewsEmployee.objects.filter(owner=self.request.user)
        context['reviews_type'] = TypeReview.objects.all()
        context['checking_review'] = ReviewsEmployee.objects.filter(check_review=ReviewsEmployee.CHECKING)
        context['reviews_negative'] = []
        for review in ReviewCountdown.objects.all():
            start_date = review.start_date
            days_left = (start_date + datetime.timedelta(days=review.days_left)) - timezone.now()
            context['reviews_negative'].append({'review': review, 'days_left': days_left.days, 'start_date': start_date})
        return context


class EditReview(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'employee/edit_review.html'
    model = ReviewsEmployee
    form_class = ReviewForm
    #Если все ок то реверс на главную таблицу
    success_url = reverse_lazy('review')

    #Проверка на валидность формы
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.save()
        return response


def add_review(request):
    if request.method == 'POST':
        # Получаем данные из запроса
        type_stuff = request.POST.get('type-stuff')
        re_login = request.POST.get('re-login')
        re_password = request.POST.get('re_password')
        re_firstname = request.POST.get('re-first-name')
        re_lastname = request.POST.get('re-last-name')
        space = request.POST.get('space')
        note = request.POST.get('re_note')
        office = request.POST.get('office')
        review_text = request.POST.get('review-text')
        type_stuff_key = ClientStuff.objects.get(id=type_stuff)
        space_key = SpaceList.objects.get(id=space)
        null_review_status = ReviewStatus.objects.get(name=ReviewStatus.NULL)

        status_review = ReviewsEmployee.GOOD
        user_pool = request.user.pool.name
        print('user_pool:', user_pool)


        if user_pool == 'Положительные':
            try:
                type_review = TypeReview.objects.get(name=TypeReview.POSITIVE)
            except TypeReview.DoesNotExist:
                type_review = TypeReview.objects.create(name=TypeReview.POSITIVE)
        elif user_pool == 'Отрицательные':
            try:
                type_review = TypeReview.objects.get(name=TypeReview.NEGATIVE)
            except TypeReview.DoesNotExist:
                type_review = TypeReview.objects.create(name=TypeReview.NEGATIVE)
        else:
            type_review_name = request.POST.get('type_review')
            if type_review_name:
                try:
                    type_review = TypeReview.objects.get(id=type_review_name)
                except TypeReview.DoesNotExist:
                    type_review = TypeReview.objects.create(name=type_review_name)
            else:
                type_review = None

        counterdown = None

        create_parts = [review_text[i:i+len(review_text)//5] for i in range(0, len(review_text), len(review_text)//5)]
        mathc_reviews = []
        review = None
        matched_review = None

        for part in create_parts:
            reviews = ReviewsEmployee.objects.filter(Q(review_text__icontains=part))
            mathc_reviews.append(reviews)
            for review in reviews:
                # Сравниваем review_text и review.review_text, игнорируя регистр
                if review_text.lower() == review.review_text.lower():
                    # Найден точно такой же отзыв
                    status_review = ReviewsEmployee.CHECKING
                    matched_review = review
                    break
                else:
                    # Сравниваем количество совпадений частей отзыва
                    match_parts = sum([1 for p in create_parts if p in review.review_text])
                    if match_parts >= 3 and match_parts <= 4:
                        status_review  = ReviewsEmployee.CHECKING
                        matched_review = review
                        break
            if matched_review is not None:
                # Если найдено совпадение, сохраняем его статус в переменную
                status_review = ReviewsEmployee.CHECKING
                review_text = matched_review.review_text
            else:
                review_text = review_text

        record = ReviewsEmployee.objects.create(
                owner=request.user,
                type_stuff=type_stuff_key,
                re_login=re_login,
                re_password=re_password,
                re_firstname=re_firstname,
                re_lastname=re_lastname,
                space = space_key,
                note = note,
                office = office,
                review_text = review_text,
                check_review = status_review,
                type_review = type_review,
                status=null_review_status
            )

        record.save()


        if type_review.name == TypeReview.NEGATIVE:
            end_date = datetime.date.today() + datetime.timedelta(days=14)
            days_left = (end_date - datetime.date.today()).days
            review = ReviewsEmployee.objects.get(id=record.id)
            counterdown = ReviewCountdown.objects.create(review=record, days_left=days_left)
            counterdown.save()
        print("counterdown", counterdown)

        # Возвращаем JsonResponse с новой записью
        data = {
            'id': record.id,
            'date': record.create_date,
            'type_stuff': record.type_stuff.name,
            're_login': record.re_login,
            're_password': record.re_password,
            're_firstname': record.re_firstname,
            're_lastname': record.re_lastname,
            'space': record.space.name,
            'note': record.note,
            'office': record.office,
            'check_review': record.check_review,
            'review_text': record.review_text,
            'type_review': record.type_review.name,
            'status': record.status.name
        }
        return JsonResponse(data)
    else:
        return HttpResponseRedirect(request.path_info)

class EmployeeView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'employee/employee_base.html'

    def get(self, request, *args, **kwargs):
        task_list = TaskerManager.objects.filter(owner=request.user)
        global_task = TaskerManager.objects.filter(global_task=True)
        context = {'task_list': task_list, 'global_task': global_task}
        return render(request, self.template_name, context=context)
    

    def post(self, request, *args, **kwargs):
        date = request.POST.get('date_task')
        text = request.POST.get('text_task')

        new_record = TaskerManager(owner=request.user, text=text, start_date=date)
        new_record.save()

        return HttpResponseRedirect(request.path_info)
    

class ObserverView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'employee/observ_base.html'

    def get(self, request, *args, **kwargs):
        empl = CustomUser.objects.filter(role=3)
        context = {'empl': empl}
        return render(request, self.template_name, context)
    
class TableView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'employee/table.html'

    def get(self, request, *args, **kwargs):
        #Если это Админ, то показать все объекты в таблице, если нет - то только те позиции которые были созданы пользователем
        if request.user.role.name == 'Администратор':
            table = TableEmpl.objects.all()
        else:
            table = TableEmpl.objects.filter(owner=request.user)
            # Получаем данные
        reviews_count = ReviewsEmployee.objects.values('owner__username').annotate(count=Count('owner__username')).order_by('-count')
        reviews = ReviewsEmployee.objects.all().count()
        type_reviews = TypeReview.objects.all()
        positive_reviews_count = []
        negative_reviews_count = []
        for type_review in type_reviews:
            positive_count = ReviewsEmployee.objects.filter(type_review=type_review, type_review__name='Позитивный').count()
            negative_count = ReviewsEmployee.objects.filter(type_review=type_review, type_review__name='Отрицательный').count()
            positive_reviews_count.append(positive_count)
            negative_reviews_count.append(negative_count)
        # Подготавливаем данные для графика
        labels = [r['owner__username'] for r in reviews_count]
        data = [r['count'] for r in reviews_count]
        chart_data = {
            'labels': labels,
            'data': data,
        }

        # Сериализуем данные
        chart_data_json = json.dumps(chart_data)
        context = {'chart_data': chart_data_json, 'reviews': reviews, 'reviews_count': reviews_count,
               'type_reviews': type_reviews, 'positive_reviews_count': positive_reviews_count,
               'negative_reviews_count': negative_reviews_count}
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        #Получаем значения из шаблона и сохраняем в переменные (значения берутся из input и аттрибут name)
        number = request.POST.get('number')
        description = request.POST.get('description')
        title = request.POST.get('title')

        #Добавление новой записи в таблицу
        new_record = TableEmpl(number=number, description=description, title=title, owner=request.user)
        new_record.save()

        return HttpResponseRedirect(request.path_info)
    
    #Сигнал для создания записи в таблице действий пользовтелей если что то было измененено или добавлено в Основную таблицу TableEmpl
    @receiver(post_save, sender=TableEmpl)
    def save_user_action(sender, instance, created, **kwargs):
        if created:
            content_type = ContentType.objects.get_for_model(sender)
            UserAction.objects.create(
                user=instance.owner,
                content_type=content_type,
                object_id=instance.id,
                action='Работа с таблицей'
            )

#Представление для обновления уже созданной записи в таблице
class EditRecordView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'employee/edit_record.html'
    model = TableEmpl
    form_class = TableEmplForm
    #Если все ок то реверс на главную таблицу
    success_url = reverse_lazy('table')

    #Проверка на валидность формы
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.save()
        return response
    

def chart_data(request):
    # Получаем данные
    reviews_count = ReviewsEmployee.objects.values('owner__username').annotate(count=Count('owner__username')).order_by('-count')

    # Подготавливаем данные для графика
    labels = [r['owner__username'] for r in reviews_count]
    data = [r['count'] for r in reviews_count]
    chart_data = {
        'labels': labels,
        'data': data,
    }

    # Сериализуем данные
    chart_data_json = json.dumps(chart_data)

    # Отображаем график
    return render(request, 'employee/table.html', {'chart_data': chart_data_json})