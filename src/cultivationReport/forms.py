from .models import CultivationReport, CultivationReportDetails
from productionReport.models import Product, LLLocation, Garden
from core import reportUtils
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML


class CultivationReportForm(forms.ModelForm):
    class Meta:
        model = CultivationReport
        fields = ["city", "location", "garden", "cultivation_date"]
        widgets = {
            "cultivation_date": forms.DateInput(attrs={"type": "date",}),
        }
        labels = {
            'cultivation_date': 'Date when the cultivation status was checked',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = LLLocation.objects.none()
        self.fields['garden'].queryset = Garden.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['location'].queryset = LLLocation.objects.filter(living_lab_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty location queryset
        elif self.instance.pk:
            self.fields['location'].queryset = LLLocation.objects.filter(living_lab=self.instance.city).order_by('name')

        if 'location'  in self.data:
            try:
                location_id = int(self.data.get('location'))
                city_id = int(self.data.get('city'))
                self.fields['garden'].queryset = Garden.objects.filter(location_id=location_id).filter(living_lab_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty location queryset
        elif self.instance.pk:
            self.fields['garden'].queryset = self.instance.location.garden_set.order_by('name')

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("city"),
                Column("location"),
                Column("garden"),
            ),
            Row(
                Column("cultivation_date"),
            ),
        )

class CultivationProductForm(forms.ModelForm):
    class Meta:
        model = CultivationReportDetails
        fields = ["name", "area_cultivated"]
        labels = {
            'name' : 'Product',
        }

    area_cultivated = forms.FloatField(label="Area cultivated")    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class' : 'product-name-select'
        })
            
        initial_unit = ""
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        "name",
                        wrapper_class="d-flex align-items-center",
                        onchange="updateUnitCultivation(this)",
                        onload="updateUnitCultivation(this)",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field("area_cultivated", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
                ),
                Column(
                    HTML(f'<div class="unit-cultivation-display"> {initial_unit} </div>'),
                    css_class="col-md-1",
                ),
                Column(
                    Button(
                        "delete",
                        "Delete",
                        css_class="btn btn-danger",
                        onclick="deleteRow(this)",
                    ),
                    css_class="col-md-3",
                ),
            )
        )
