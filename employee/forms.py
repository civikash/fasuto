from django import forms
from adminc.models import ReviewsEmployee
from employee.models import TableEmpl
from adminc.models import ReviewStatus, TypeReview, ReviewsEmployee

#Форма для редактирования записи в таблице

class TableEmplForm(forms.ModelForm):
    class Meta:
        model = TableEmpl #Что за модель
        fields = ['number', 'description', 'title'] #Какие поля (мы не должны указывать поле owner)
    
    #здесь идет отображение значений, которые относятся к этому объекту (предзагрузка информации)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['number'].widget.attrs['value'] = instance.number
            self.fields['description'].widget.attrs['value'] = instance.description
            self.fields['title'].widget.attrs['value'] = instance.title


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewsEmployee #Что за модель
        fields = ['review_text', 'office'] #Какие поля (мы не должны указывать поле owner)
    
    #здесь идет отображение значений, которые относятся к этому объекту (предзагрузка информации)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['review_text'].widget.attrs['value'] = instance.review_text


class ReviewsEmployeeFilterForm(forms.Form):
    client = forms.CharField(max_length=35, required=False, label='Тип')
    re_login = forms.CharField(max_length=35, required=False, label='Логин')
    re_username = forms.CharField(max_length=35, required=False, label='Пользователь')
    office = forms.CharField(max_length=300, required=False, label='Площадка')
    type_review = forms.ModelChoiceField(queryset=TypeReview.objects.all(), empty_label=None, required=False, label='Тип')
    status = forms.ModelChoiceField(queryset=ReviewStatus.objects.all(), empty_label=None, required=False,label='Статус')