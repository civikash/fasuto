from django.contrib import admin
from django.urls import path
from employee.views import EmployeeView, add_review, CheckOneServiceView, CheckAllServiceView, TableView, EditRecordView, EditReview, CheckServiceView, ObserverView, TableReviewView

urlpatterns = [
    path('emp/', EmployeeView.as_view(), name='employee'),
    path('observer/', ObserverView.as_view(), name='observ_emp'),
    path('table/', TableView.as_view(), name='table'),
    path('review/checking', CheckServiceView.as_view(), name='check_service'),
    path('review/checking_all', CheckAllServiceView.as_view(), name='check_all_service'),
    path('review/checking_parce', CheckOneServiceView.as_view(), name='check_solo_parce'),
    path('review/', TableReviewView.as_view(), name='review'),
    path('review/edit/<int:pk>/', EditReview.as_view(), name='edit_review'),
    path('review/add-review/', add_review, name='review_add'),
    path('record/edit/<int:pk>/', EditRecordView.as_view(), name='edit_record'),
]