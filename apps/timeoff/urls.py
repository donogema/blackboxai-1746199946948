from django.urls import path
from . import views

app_name = 'timeoff'

urlpatterns = [
    path('list/', views.timeoff_list, name='timeoff_list'),
    path('apply/', views.timeoff_apply, name='timeoff_apply'),
    path('review/<int:pk>/', views.timeoff_review, name='timeoff_review'),
]
