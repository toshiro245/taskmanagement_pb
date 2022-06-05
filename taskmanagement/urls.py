from django.urls import path

from .views import (
    HomeView, TaskCreateView, task_delete, TaskUpdateView, TaskConductView,
    task_record, MemoUpdateView, get_record, RecordCreateView, RecordUpdateView,
    record_delete, get_total_record, 
)

app_name = 'taskmanagement'

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('task_create', TaskCreateView.as_view(), name='task_create'),
    path('task_delete', task_delete, name='task_delete'),
    path('task_update/<int:pk>', TaskUpdateView.as_view(), name='task_update'),
    path('task_conduct/<int:pk>', TaskConductView.as_view(), name='task_conduct'),
    path('task_record/', task_record, name='task_record'),
    path('update_memo/<int:pk>', MemoUpdateView.as_view(), name='update_memo'),
    path('get_record/', get_record, name='get_record'),
    path('record_create/', RecordCreateView.as_view(), name='record_create'),
    path('record_update/<int:pk>', RecordUpdateView.as_view(), name='record_update'),
    path('record_delete', record_delete, name='record_delete'),
    path('get_total_record', get_total_record, name='get_total_record'),
]
