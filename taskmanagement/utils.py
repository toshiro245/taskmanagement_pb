import copy
import pytz
import datetime
from django.utils import timezone
from django.db.models import Sum

from taskmanagement.models import TaskItems, TaskRecords


def one_subject_record(user, task_id, offset):
    country = user.country
    today_utc = timezone.now()

    today_local = today_utc.astimezone(pytz.timezone(country))
    last_day = today_local.replace(hour=23, minute=59, second=59)
    period_days = offset
    days = []
    
    for day in range(period_days):
        day_local = (today_local + datetime.timedelta(days=-day)).strftime('%Y-%m-%d')
        days.append(day_local)
    days.reverse()
    data_tmp = {day:0 for day in days}

    task_records = TaskRecords.objects.filter(
        task__user=user.id,
        task=task_id,
        study_at_local__gte=days[0],
        study_at_local__lte=last_day
    ).all()

    task_item = TaskItems.objects.filter(
        id=task_id,
        user=user
    ).first()

    label = task_item.task_name

    task_records_sorted = task_records.values('study_at_local').annotate(
        total_time=Sum('time_total_second')
    ).order_by('study_at_local')

    for task_record in task_records_sorted:
        data_tmp[task_record['study_at_local']] = task_record['total_time']
    
    data_record = []
    for day, task_record in data_tmp.items():
        data_record.append(task_record)

    datasets = [{
        'label': label,
        'data': data_record,
        'backgroundColor': 'rgba(48, 48, 47, 0.9)',
        'borderColor': "#0a0a0a",
    }]
    data = {}
    data['labels'] = days
    data['datasets'] = datasets

    return data



def all_subject_record(user, offset):
    country = user.country
    today_utc = timezone.now()

    today_local = today_utc.astimezone(pytz.timezone(country))
    last_day = today_local.replace(hour=23, minute=59, second=59)
    period_days = offset
    days = []

    for day in range(period_days):
        day_local = (today_local + datetime.timedelta(days=-day)).strftime('%Y-%m-%d')
        days.append(day_local)
    days.reverse()
    data_tmp = {day:0 for day in days}

    task_records = TaskRecords.objects.filter(
        study_at_local__gte=days[0],
        study_at_local__lte=last_day,
        task__user = user.id,
    ).all()

    sorted_task_records = task_records.order_by('task_id').values('task')
    task_id_list = []
    for task_record_item in sorted_task_records:
        task_id = task_record_item['task']
        if task_id not in task_id_list:
            task_id_list.append(task_id)
    
    task_records_dict = {task_id:[] for task_id in task_id_list}

    for date in days:
        task_record_oneday = task_records.filter(study_at_local__contains=date).all()

        if not task_record_oneday:
            for task_record_value in task_records_dict.values():
                task_record_value.append(0)
            continue

        sorted_task_record_oneday = task_record_oneday.values('task_id').annotate(
            total_time = Sum('time_total_second')
        ).order_by('task_id')

        check_task_id_list = copy.copy(task_id_list)
        for sorted_task_record_item in sorted_task_record_oneday:

            for task_id in task_id_list:
                if sorted_task_record_item['task_id'] == task_id:
                    task_records_dict[task_id].append(sorted_task_record_item['total_time'])
                    check_task_id_list.remove(task_id)
                    break

        for task_id in check_task_id_list:
            task_records_dict[task_id].append(0)


    # json data
    datasets = []
    pre_dict = {}
    for task_id, task_record in task_records_dict.items():
        query = TaskItems.objects.filter(id=task_id).first()
        pre_dict['label'] = query.task_name
        pre_dict['data'] = task_record
        pre_dict['backgroundColor'] = query.color
        pre_dict['borderWidth'] = 0
        datasets.append(pre_dict)
        pre_dict = {}

    # json data
    data = {}
    data['labels'] = days
    data['datasets'] = datasets

    return data