from django import forms
from .models import SalaryAdvance

class SalaryAdvanceForm(forms.ModelForm):
    class Meta:
        model = SalaryAdvance
        fields = ['requested_amount', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }
