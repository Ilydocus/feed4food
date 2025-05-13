from .models import WaterReport, WaterReportIrrigation, WaterReportRainfall
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
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    quantity = forms.FloatField(label="Quantity")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unit = "L"
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
                        "period",
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
                    Field("frequency_times", wrapper_class="d-flex align-items-center"),
                    HTML('times a '),
                    Field("frequency_interval", wrapper_class="d-flex align-items-center"),
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






