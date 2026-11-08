from django.db import models
from django.conf import settings

# Create your models here.
class Todo_task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='todo_tasks',
        null=True,
        blank=True,
        editable=False,
    )
    title = models.CharField(max_length=50)
    discription = models.CharField(max_length=500,blank=True )
    category = models.CharField(max_length=30)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
