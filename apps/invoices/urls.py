from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('list/', views.invoice_list, name='invoice_list'),
    path('create/', views.invoice_create, name='invoice_create'),
    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('<int:pk>/export/pdf/', views.export_invoice_pdf, name='export_invoice_pdf'),
    path('<int:pk>/export/excel/', views.export_invoice_excel, name='export_invoice_excel'),
]
