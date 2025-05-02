from django import forms
from .models import OrganizationProfile

class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = [
            'organization_name',
            'logo',
            'enable_invoices',
            'enable_customers',
            'enable_reports',
            'enable_leave',
            'enable_timeoff',
            'enable_salaryadvance',
        ]
