from django.urls import path
from . import views


app_name = 'TODO'

urlpatterns = [
    path('all_task', views.all_task, name='all_task'),
    path('add_task', views.add_task, name='add_task'),
    path('edit_task/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:pk>/', views.delete_task, name='delete_task'),
]
