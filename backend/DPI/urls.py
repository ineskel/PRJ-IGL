from django.urls import path
from .views import DPIView

urlpatterns = [
    path('createDPI/', DPIView.as_view(), name='createDPI'),
]
