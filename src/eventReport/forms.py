from .models import EventReport, EventPersonDetails, UnderrepresentedGroup
from core import reportUtils
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML


class EventReportForm(forms.ModelForm):
    class Meta:
        model = EventReport
        fields = ["city", "event_date", "event_name", "event_loc", 
                  "event_type", "event_desc", "currency", "event_costs", 
                  "event_costs_desc", "event_revenues", "event_revenues_desc"]
        widgets = {
            "event_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.fields['city'].label = "Organizing living lab"
        self.fields['event_loc'].label = "Event location"
        self.fields['event_desc'].label = "Event description"
        self.fields['event_costs_desc'].label = "Description"
        self.fields['event_revenues_desc'].label = "Description"

        self.fields['city'].widget.attrs.update({
            'id': 'id_city',
            'onchange': 'updateGroupOptions()'
        })

        self.helper.layout = Layout(
            Row(  
                Column("city"),            
                Column("event_date"),
                Column("event_name"),
            ),
            Row(
                Column(Field("event_loc")),
                Column("event_type"),
                Column("event_desc"),
            ),
            Row(
                    HTML(f'<h3> Economy </h3>'),
                    css_class="col-md-1",
                ),
            Row(
                Column(
                    Field("currency", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
                ),
            ),
            Row(
                Column(
                    Field("event_costs", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
                ),
                Column(
                    Field("event_costs_desc", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
                ),
            ),
            Row(
                Column(
                    Field("event_revenues", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
                ),
                Column(
                    Field("event_revenues_desc", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
                ),
            ),
        )

class EventPersonForm(forms.ModelForm):
    class Meta:
        model = EventReport
        fields = ["total_invited", "total_participant"]

    total_invited = forms.IntegerField(label="Total number of invited persons")
    total_participant = forms.IntegerField(label="Total number of participants")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        "total_invited",
                        wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field(
                        "total_participant",
                        wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-3",
                ),
            )
        )

class EventPersonDetailsForm(forms.ModelForm):
    class Meta:
        model = EventPersonDetails
        fields = ["name", "number_invited", "number_participant"]

    number_invited = forms.IntegerField(label="Number of invited persons for this group")
    number_participant = forms.IntegerField(label="Number of participants for this group")
    

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
        #self.fields['name'].choices = get_underrepresentedgroup_choices()

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
                    Field("number_invited", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
                ),
                Column(
                    Field("number_participant", wrapper_class="d-flex align-items-center"),
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
