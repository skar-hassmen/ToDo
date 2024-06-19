from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin


class Tasks(models.Model):
    class Meta:
        db_table = "Задачи"
    title = models.CharField("Заголовок задачи", max_length=50)
    date_deadline = models.DateField("Дата дедлайна")
    status = models.PositiveIntegerField("Статус задачи", default=0)
    description = models.TextField("Описание задачи")
    priority = models.PositiveIntegerField("Приоритет задачи", default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class TasksAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'id')
    search_fields = ('user',)