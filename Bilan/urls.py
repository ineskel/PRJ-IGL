from django.urls import path
from . import views

urlpatterns = [
    path('biologique/<int:pk>/', views.create_bilanbiologique, name='create_bilanbiologique'),
    path('radiologique/<int:pk>/', views.create_bilanradiologique, name='create_bilanradiologique'),
]