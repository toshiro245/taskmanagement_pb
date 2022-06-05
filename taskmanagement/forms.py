from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput


from .models import TaskItems, Memo, TaskRecords


COLOR_CHOICES = (
    ('rgba(25, 247, 214)', 'LightGreen'),
    ('rgba(118, 118, 245)', 'LightBlue'),
    ('rgba(32, 54, 250)', 'Blue'),
    ('rgba(200, 130, 250)', 'Purple'),
    ('rgba(235, 199, 199)', 'Peach'),
    ('rgba(250, 76, 40)', 'Red'),
    ('rgba(247, 139, 7)', 'Orange'),
    ('rgba(252, 3, 227)', 'Pink'),
)


class TaskCreateForm(forms.ModelForm):
    task_name = forms.CharField(label='Task Title')
    color = forms.ChoiceField(choices=COLOR_CHOICES)

    class Meta:
        model = TaskItems
        fields = ('task_name', 'color')

    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs['class'] = 'form-control'
        self.fields['color'].widget.attrs['class'] = 'form-color'
        self.fields['task_name'].widget.attrs['placeholder'] = str(self.fields['task_name'].label) + '*'
    

    def save(self, commit=False):
        item = super().save(commit=False)
        item.user = self.user
        item.save()
        return item


class TaskUpdateForm(forms.ModelForm):
    task_name = forms.CharField(label='Task Title')
    color = forms.ChoiceField(choices=COLOR_CHOICES)

    class Meta:
        model = TaskItems
        fields = ('task_name', 'color')

    def __init__(self, *args, **kwargs):
        super(TaskUpdateForm, self).__init__(*args, **kwargs)
        self.fields['task_name'].widget.attrs['class'] = 'form-control'
        self.fields['color'].widget.attrs['class'] = 'form-color'
        self.fields['task_name'].widget.attrs['placeholder'] = str(self.fields['task_name'].label) + '*'


class MemoUpdateForm(forms.ModelForm):
    # memo = forms.CharField(widget=forms.Textarea(attrs={'cols':'80', 'rows': '10'}), required=False)
    memo = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(MemoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['memo'].widget.attrs['class'] = 'form-control'
        

    class Meta:
        model = Memo
        fields = ('memo', )
    


class RecordCreateForm(forms.ModelForm):
    time_hour = forms.IntegerField()
    time_min = forms.IntegerField()

    class Meta:
        model = TaskRecords
        fields = ('task', 'time_hour', 'time_min')

    def __init__(self, *args, **kwargs):
        super(RecordCreateForm, self).__init__(*args, **kwargs)
        self.fields['task'].widget.attrs['class'] = 'form-control'
        self.fields['time_hour'].widget.attrs['class'] = 'form-color'
        self.fields['time_min'].widget.attrs['class'] = 'form-color'
        


    def save(self, commit=False):
        record = super().save(commit=False)
        
        time_min = self.cleaned_data['time_min']
        time_hour = self.cleaned_data['time_hour']
        time_total_second = time_hour*3600 + time_min*60
        
        record.time_total_second = time_total_second
        record.save()
        return record


class RecordUpdateForm(forms.ModelForm):
    time_hour = forms.IntegerField()
    time_min = forms.IntegerField()

    class Meta:
        model = TaskRecords
        fields = ('task', 'time_hour', 'time_min')

    def __init__(self, *args, **kwargs):
        super(RecordUpdateForm, self).__init__(*args, **kwargs)
        self.fields['task'].widget.attrs['class'] = 'form-control'
        self.fields['time_hour'].widget.attrs['class'] = 'form-color'
        self.fields['time_min'].widget.attrs['class'] = 'form-color'

    
    def save(self, commit=False):
        record = super().save(commit=False)
        time_min = self.cleaned_data['time_min']
        time_hour = self.cleaned_data['time_hour']
        time_total_second = time_hour*3600 + time_min*60    
        record.time_total_second = time_total_second
        record.save()
        return record