from .models import PlantingReport, PlantingReportDetails
from productionReport.models import Product, LLLocation, Garden
from core import reportUtils
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML


class PlantingReportForm(forms.ModelForm):
    class Meta:
        model = PlantingReport
        fields = ["city", "location", "garden", "planting_date"]
        widgets = {
            "planting_date": forms.DateInput(attrs={"type": "date",}),
        }
        labels = {
            'planting_date': 'Date when the planting was done',
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
                Column("planting_date"),
            ),
        )

class PlantingProductForm(forms.ModelForm):
    class Meta:
        model = PlantingReportDetails
        fields = ["name", "area_quantity_planted", "planting_unit"]
        labels = {
            'name' : 'Product',
        }

    area_quantity_planted = forms.FloatField(label="Area/Quantity planted")   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class' : 'product-name-select'
        })
            
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        "name",
                        wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field("area_quantity_planted", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
                ),
                Column(
                    Field("planting_unit", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
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
