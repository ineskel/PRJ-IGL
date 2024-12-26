from django.urls import path
from . import views

urlpatterns = [
    path('', views.MedicamentList.as_view(), name='medicament_list'),
    path('delete/<int:pk>/', views.MedicamentList.as_view(), name='medicament_delete'),
    path('add', views.MedicamentList.as_view(), name='medicament_add'),  
]