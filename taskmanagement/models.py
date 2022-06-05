from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class TaskItems(models.Model):
    task_name = models.CharField(max_length=60)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    color = models.CharField(max_length=50)
    

    class Meta:
        db_table = 'task_items'
        unique_together = ('task_name', 'user')

    def __str__(self):
        return f'{self.task_name}'


class TaskRecords(models.Model):
    time_total_second = models.IntegerField()
    time_min = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(59)])
    time_hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    task = models.ForeignKey(
        TaskItems, on_delete=models.CASCADE
    )
    study_at_local = models.CharField(max_length=100)

    class Meta:
        db_table = 'task_records'

    def __str__(self):
        return f'{self.task.task_name}({self.time_total_second}s)'


class Memo(models.Model):
    memo = models.TextField(null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'memo'
    
    def __str__(self):
        return f'{self.user.email}'