from .models import LLUseReport, LLUseReportPerUnderrepresentedGroups
from demographicReport.models import UnderrepresentedGroup 
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML


class LLUseReportForm(forms.ModelForm):
    class Meta:
        model = LLUseReport
        fields = ["city", "report_date", "gardens_in_use", "total_ll_participants"]
        widgets = {
            "report_date": forms.DateInput(attrs={"type": "date"}),
        } 
    gardens_in_use = forms.IntegerField(label="Gardens or holdings in use")
    total_ll_participants = forms.IntegerField(label="Total number of Living Lab participants")  

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
                Column("report_date"),
            ),
            Row(
                Column("gardens_in_use"),
            ),
            Row(
                Column("total_ll_participants"),
            ),
        )


class LLUseGroupForm(forms.ModelForm):
    class Meta:
        model = LLUseReportPerUnderrepresentedGroups
        fields = ["name", "ll_participants"]

    ll_participants = forms.IntegerField(label="Living Lab participants") 

    def __init__(self, *args, **kwargs):
        # Extract city parameter if provided
        city = kwargs.pop('city', None)
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'id': 'id_group-name-select',
        }) 

        # Filter the name field queryset based on city
        if city:
            self.fields['name'].queryset = UnderrepresentedGroup.objects.filter(
                living_lab=city
            )
        else:
            # If no city provided, show empty queryset 
            self.fields['name'].queryset = UnderrepresentedGroup.objects.none()
        
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
                    Field("ll_participants", wrapper_class="d-flex align-items-center"),
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
