from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'text']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a comment...'}),
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ['username', 'email', 'password1', 'password2']
