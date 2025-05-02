from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('dashboard/', views.report_dashboard, name='report_dashboard'),
    path('export/pdf/', views.export_report_pdf, name='export_report_pdf'),
    path('export/excel/', views.export_report_excel, name='export_report_excel'),
]
