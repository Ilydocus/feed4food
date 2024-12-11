from django import forms
from .models import ProduceReport

class ProduceReportForm(forms.ModelForm):
    class Meta:
        model = ProduceReport
        fields = ['farmer_name', 'produce_type', 'quantity']
