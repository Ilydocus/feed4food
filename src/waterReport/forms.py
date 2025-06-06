from .models import WaterReport, WaterReportIrrigation, WaterReportRainfall
from productionReport.models import LLLocation, Garden
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML


class WaterReportForm(forms.ModelForm):
    class Meta:
        model = WaterReport
        fields = ["city", "location", "garden"]

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
            self.fields['location'].queryset = self.instance.city.location_set.order_by('name')

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
        )


class WaterRainfallForm(forms.ModelForm):
    class Meta:
        model = WaterReportRainfall
        fields = ["start_date", "end_date", "quantity"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "label":"Rainfall start date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    quantity = forms.FloatField(label="Quantity")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unit = "L"
        self.fields['start_date'].label = "Rainfall start date"
        self.fields['end_date'].label = "Rainfall end date"
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        "start_date",
                        wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field(
                        "end_date",
                        wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field("quantity", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
                ),
                Column(
                    HTML(f'<div class="unit-display"> {unit} </div>'),
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

class WaterIrrigationForm(forms.ModelForm):
    class Meta:
        model = WaterReportIrrigation
        fields = ["start_date", "end_date", "frequency_times", "frequency_interval", "period", "quantity"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "period": forms.CheckboxInput()
        }

    quantity = forms.FloatField(label="Quantity")
    frequency_times=forms.FloatField(label="Frequency") 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unit = "L"
        self.fields['frequency_interval'].label = False
        self.fields['frequency_interval'].widget.attrs['class'] = 'interval'
        self.fields['start_date'].label = "Date"
        self.fields['period'].label = "Use over a period"
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field("quantity", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
                ),
                Column(
                    HTML(f'<div class="unit-display"> {unit} </div>'),
                    css_class="col-md-1",
                ),
                Column(
                    Field(
                        "start_date",
                        wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-2",
                ),
                Column(
                    Field(
                        "period",
                        wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-1",
                ),
                Column(
                    Field(
                        "end_date",
                        wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-2",
                ),                
                Column(
                    Field("frequency_times", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-2",
                ),
                Column(
                    HTML('<div class="times-display"> times a </div>'),
                    css_class="col-md-1",
                ),
                Column(
                    Field("frequency_interval", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-2",
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
                css_class="irrigation_row",
            )
        )






