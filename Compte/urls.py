from django.urls import path
from . import views
from .views import test_connection

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('test-connection/', test_connection, name='test-connection'),
]