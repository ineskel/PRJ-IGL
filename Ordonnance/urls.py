from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.Ordonnances , name='Ordonnances'),
    path('<int:pk>/', views.Ordonnanceid, name='Ordonnanceid'),
    path('add/', views.OrdonnanceAdd, name='OrdonnanceAdd'),
    path('Delete/<int:pk>/', views.OrdonnanceDelete, name='OrdonnanceDelete'),
    path('attente/', views.OrdonnanceAttente, name='OrdonnanceAttente'),
    path('valide/<int:pk>/', views.OrdonnanceValide, name='OrdonnanceValide'),
    path('nonvalide/<int:pk>/', views.OrdonnanceNonValide, name='OrdonnanceNonValide'),
]