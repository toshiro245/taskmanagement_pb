import json
import pytz
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, JsonResponse

from taskmanagement.models import TaskItems, TaskRecords, Memo
from .forms import (
    TaskCreateForm, TaskUpdateForm, MemoUpdateForm, RecordCreateForm,
    RecordUpdateForm,
)
from .utils import one_subject_record, all_subject_record


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'taskmanagement/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        tasks = TaskItems.objects.filter(
            user=user, 
        ).all()
        task_length = len(tasks)
        memo = get_object_or_404(Memo, user=self.request.user)

        task_records = TaskRecords.objects.filter(
            task__user=user,
        ).order_by('-study_at_local')[:7]
        
        all_record = all_subject_record(user, 7)

        context = {
            'tasks': tasks,
            'task_length': task_length,
            'memo': memo,
            'task_records': task_records,
            'data' : json.dumps(all_record),
        }

        return context
    


class TaskCreateView(LoginRequiredMixin, CreateView):
    template_name = 'taskmanagement/task_create.html'
    model = TaskItems
    form_class = TaskCreateForm
    success_url = reverse_lazy('taskmanagement:home')

    def get(self, request, *args, **kwargs):
        tasks = TaskItems.objects.filter(
            user=self.request.user
        ).all()
        if(len(tasks)) >= 8:
            return redirect('taskmanagement:home')
        else:
            return super().get(request, *args, **kwargs)


    def form_valid(self, form):
        try:
            form.user = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('task_name', 'The title already exsists')
            return render(self.request, 'tasks/task_create.html', context={
                'form': form,
            })


@login_required
def task_delete(request):
    if request.method == "POST":
        task_id = request.POST['task_id']
        if task_id:
            task = get_object_or_404(TaskItems, pk=task_id, user=request.user.id)
            task.delete()
            return redirect(reverse_lazy('taskmanagement:home'))
        
        else:
            return redirect('taskmanagement:home')
    
    raise Http404


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'taskmanagement/task_update.html'
    model = TaskItems
    form_class = TaskUpdateForm
    success_url = reverse_lazy('taskmanagement:home')



class TaskConductView(LoginRequiredMixin, TemplateView):
    template_name = 'taskmanagement/task_conduct.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(TaskItems, pk=kwargs.get('pk'), user=self.request.user)
        context['task'] = task
        return context


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def task_record(request):
    if request.method == 'POST':
        record = request.POST.get('record')
        task_id = int(request.POST.get('task_id'))
        time_hour = int(record[:2])
        time_min = int(record[3:5])
        time_total_second = int(record[:2])*3600 + int(record[3:5])*60 + int(record[6:])
        now_utc = timezone.now()
        user = request.user
        now_local = now_utc.astimezone(pytz.timezone(user.country))
        TaskRecords.objects.create(
            time_total_second = time_total_second,
            time_min = time_min,
            time_hour = time_hour,
            task_id=task_id,
            study_at_local=now_local.date(),
        )

        if is_ajax(request=request):
            return JsonResponse({})


class MemoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'taskmanagement/update_memo.html'
    model = Memo
    form_class = MemoUpdateForm
    success_url = reverse_lazy('taskmanagement:home')


@login_required
def get_record(request):
    if request.method == 'POST':
        task_id = request.POST['task_id']
        offset = int(request.POST['offset'])
        user = request.user
        data = one_subject_record(user, task_id, offset)

    if is_ajax(request=request):
        return JsonResponse({'data': data}, safe=False)
    


class RecordCreateView(LoginRequiredMixin, CreateView):
    template_name = 'taskmanagement/record_create.html'
    form_class = RecordCreateForm
    model = TaskRecords
    success_url = reverse_lazy('taskmanagement:home')

    def form_valid(self, form):
        study_at_local = self.request.POST.get('study_at_local')
        form.instance.study_at_local = study_at_local
        form.save()
        return super(RecordCreateView, self).form_valid(form)



class RecordUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'taskmanagement/record_update.html'
    model = TaskRecords
    form_class = RecordUpdateForm
    success_url = reverse_lazy('taskmanagement:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_record = get_object_or_404(TaskRecords, pk=self.kwargs['pk'], task__user=self.request.user)
        context['task_record'] = task_record
        return context

    def form_valid(self, form):
        study_at_local = self.request.POST.get('study_at_local')
        form.instance.study_at_local = study_at_local
        form.save()
        return super(RecordUpdateView, self).form_valid(form)


@login_required
def record_delete(request):
    if request.method == "POST":
        task_record_id = request.POST['task_record_id']
        if task_record_id:
            task = get_object_or_404(TaskRecords, pk=task_record_id, task__user=request.user.id)
            task.delete()
            return redirect(reverse_lazy('taskmanagement:home'))
        
        else:
            return redirect('taskmanagement:home')
    
    raise Http404


@login_required
def get_total_record(request):
    if request.method == 'POST':
        offset = int(request.POST['offset'])
        user = request.user
        data = all_subject_record(user, offset)

    if is_ajax(request=request):
        return JsonResponse({'data': data}, safe=False)


# 404error
def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)