from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('organization-profile/', views.organization_profile, name='organization_profile'),
]
