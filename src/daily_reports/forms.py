from .models import ProduceReport, Items
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Button, Field

class ProduceReportForm(forms.ModelForm):
    class Meta:
        model = ProduceReport
        fields = ['start_date', 'end_date', 'city', 'location', 'garden']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('city'),
                Column('location'),
                Column('garden'),
            ),
            Row(
                Column('start_date'),
                Column('end_date'),
            ),
        )
        
class CustomSelect(Select):
    def __init__(self, *args, **kwargs):
        self.item_units = kwargs.pop('item_units', {})
        super().__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if value in self.item_units:
            option['attrs']['data-unit'] = self.item_units[value]
        if value == '':
            option['attrs']['disabled'] = 'disabled'
        return option
        
class ProduceItemForm(forms.Form):
    ITEM_CHOICES = [(item, item) for item in Items.objects.values_list('name', flat=True )]
    ITEM_CHOICES.insert(0, ('', 'Select Item'))
    ITEM_UNITS = {item: unit for (item, unit) in Items.objects.values_list('name', 'unit')}
    item = forms.ChoiceField(choices=ITEM_CHOICES, label='Item', widget=CustomSelect(item_units=ITEM_UNITS))
    quantity = forms.IntegerField(label='Quantity')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column(Field('item', wrapper_class="d-flex align-items-center", onchange="updateUnit(this)", onload="updateUnit(this)"), css_class="col-md-3"),
                Column(Field('quantity', wrapper_class="d-flex align-items-center"), css_class="col-md-3"),
                Column(Div(css_class='unit-display'), css_class="col-md-1"),
                Column(Button('delete', 'Delete', css_class='btn btn-danger', onclick="deleteRow(this)"), css_class="col-md-3"),
            )
        )