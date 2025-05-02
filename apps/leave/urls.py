from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
    path('list/', views.leave_list, name='leave_list'),
    path('apply/', views.leave_apply, name='leave_apply'),
    path('review/<int:pk>/', views.leave_review, name='leave_review'),
]
