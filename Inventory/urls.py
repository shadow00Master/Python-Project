from django.urls import path
from . import views
app_name = 'Inventory'

urlpatterns = [
    path('', views.all_Product, name= 'all_Product'),
    path('add_Product/', views.add_Product, name='add_Product'),
    path('update_Product/<int:pk>/', views.update_Product, name='update_Product'),
    path('delete_Product/<int:pk>/', views.delete_Product, name='delete_Product'),
    
]
