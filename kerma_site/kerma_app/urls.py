from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dicom/', views.show_dicom_results, name='dicom_results'),
    path('dynalog/', views.show_dynalog_results, name='dynalog_results'),
]
