from django.contrib import admin
from .models import TaskItems, TaskRecords, Memo


admin.site.register(TaskItems)
admin.site.register(TaskRecords)
admin.site.register(Memo)
