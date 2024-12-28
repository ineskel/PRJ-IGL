from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.Ordonnances , name='Ordonnances'),
    path('<int:pk>/', views.Ordonnanceid, name='Ordonnanceid'),
    path('add/', views.OrdonnanceAdd, name='OrdonnanceAdd'),
    path('Delete/<int:pk>/', views.OrdonnanceDelete, name='OrdonnanceDelete'),
]