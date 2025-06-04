from .models import DemographicReport, DemographicReportPerUnderrepresentedGroups, UnderrepresentedGroups
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML


class DemographicReportForm(forms.ModelForm):
    class Meta:
        model = DemographicReport
        fields = ["city", "data_date", "total_population"]
        widgets = {
            "data_date": forms.DateInput(attrs={"type": "date"}),
        } 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False

        self.fields['city'].widget.attrs.update({
            'id': 'id_city',
            'onchange': 'updateGroupOptions()'
        })

        self.helper.layout = Layout(
            Row(
                Column("city"),
                Column("data_date"),
            ),
            Row(
                Column("total_population"),
            ),
        )


class DemographicGroupForm(forms.ModelForm):
    class Meta:
        model = DemographicReportPerUnderrepresentedGroups
        fields = ["name", "population"]

    population = forms.IntegerField(label="Population") 

    def __init__(self, *args, **kwargs):
        # Extract city parameter if provided
        city = kwargs.pop('city', None)
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'id': 'id_group-name-select',
        }) 

        # Filter the name field queryset based on city
        if city:
            self.fields['name'].queryset = UnderrepresentedGroups.objects.filter(
                living_lab=city
            )
        else:
            # If no city provided, show empty queryset 
            self.fields['name'].queryset = UnderrepresentedGroups.objects.none()
        
        # Add CSS class for JavaScript targeting
        self.fields['name'].widget.attrs.update({
            'class': 'group-name-select'
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
                    Field("population", wrapper_class="d-flex align-items-center"),
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
