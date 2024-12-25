from django.urls import path
from . import views

urlpatterns = [
    path('Create/', views.DPIView.as_view(), name='CreateDPI'),
    path('all/', views.DPIList.as_view(), name='DPIs'),
    path('<int:NSS>/', views.ConsulterDPI.as_view(), name='ConsulterDPI'),
]