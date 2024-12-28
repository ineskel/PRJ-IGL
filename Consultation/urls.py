from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_consultation, name='create_consultation'),
    path('get/', views.get_consultations, name='get_consultations'),
    path('get/<int:pk>/', views.get_consultation_byid, name='get_consultation_medecin'),
    path('update/<int:pk>/', views.UpdateConsultation, name='UpdateConsultation'),
    path('add_ordonnance/<int:pk>/', views.add_ordonnance, name='add_ordonnance'),
]