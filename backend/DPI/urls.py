from django.urls import path
from .views import DPIView , DPIByNSSView

urlpatterns = [
    path('createDPI/', DPIView.as_view(), name='createDPI'),
    path('getDPI/', DPIView.as_view(), name='getDPI'),
    path('getDPI/<int:NSS>/',DPIByNSSView.as_view(), name='getDPIByNSS'),
]
