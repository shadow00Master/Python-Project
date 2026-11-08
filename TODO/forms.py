from django import forms
from .models import Todo_task


class Task_Form(forms.ModelForm):
    class Meta:
        model = Todo_task
        fields = ['title', 'discription', 'category','due_date']