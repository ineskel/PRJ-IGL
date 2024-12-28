from django.urls import path
from . import views

urlpatterns = [
    path('biologique/<int:pk>/', views.create_bilanbiologique, name='create_bilanbiologique'),
    path('radiologique/<int:pk>/', views.create_bilanradiologique, name='create_bilanradiologique'),
    path('demande/', views.create_demandebilan, name='create_demandebilan'),
    path('demande/all', views.getdemandesbilan, name='getdemandesbilan'),
    path('demande/treat/<int:pk>/', views.treatdemandesbilan, name='treatdemande'),
]