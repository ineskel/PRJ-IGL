from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('change_password', views.change_password, name='change_password'),
    path('get_medecins', views.get_medecins, name='get_medecins'),
    path('get_patients', views.get_patients, name='get_patients'),
    path('get_users', views.get_users, name='get_medecin'),
]