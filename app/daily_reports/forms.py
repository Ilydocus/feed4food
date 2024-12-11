from django import forms
from .models import ProduceReport

class ProduceReportForm(forms.ModelForm):
    class Meta:
        model = ProduceReport
        fields = ['farmer_name', 'produce_type', 'quantity']

from .models import Item

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)

class ItemSelectionForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all(), required=True)

class ItemDetailForm(forms.Form):
    breed = forms.CharField(max_length=255, required=False)  # Optional, dynamic
    quantity = forms.IntegerField(min_value=1, required=False)
