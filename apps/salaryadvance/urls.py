from django.urls import path
from . import views

app_name = 'salaryadvance'

urlpatterns = [
    path('list/', views.salaryadvance_list, name='salaryadvance_list'),
    path('request/', views.salaryadvance_request, name='salaryadvance_request'),
    path('review/<int:pk>/', views.salaryadvance_review, name='salaryadvance_review'),
]
