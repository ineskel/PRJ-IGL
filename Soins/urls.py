from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_soin, name='create_soin'),
    path('update/<int:IdSoin>/', views.update_soin, name='update_soin'),
    
]