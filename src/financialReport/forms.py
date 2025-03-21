from .models import FinancialReport
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML


class FinancialReportForm(forms.ModelForm):
    class Meta:
        model = FinancialReport
        fields = ["start_date", "end_date", "city", "location", "garden", "exp_workforce", 
        "exp_purchase", "exp_others", "exp_others_desc", "fun_feed4food", "fun_others", "fun_others_desc", 
        "rev_production", "rev_restaurant","rev_events", "rev_others", "rev_others_desc"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exp_workforce'].label = "Workforce costs"
        self.fields['exp_purchase'].label = "Purchase costs"
        self.fields['exp_others'].label = "Other costs"
        self.fields['exp_others_desc'].label = "Short description"
        self.fields['fun_feed4food'].label = "FEED4FOOD funding"
        self.fields['fun_others'].label = "Other funding"
        self.fields['fun_others_desc'].label = "Short description"
        self.fields['rev_production'].label = "Production sales"
        self.fields['rev_restaurant'].label = "Sales in restaurant"
        self.fields['rev_events'].label = "Revenues from events"
        self.fields['rev_others'].label = "Other revenues"
        self.fields['rev_others_desc'].label = "Short description"
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
                Column("start_date"),
                Column("end_date"),
            ),
            HTML('<h3>Expenses</h3>'),
            Row("exp_workforce",), #TODO add unit
            Row("exp_purchase",), #TODO add unit
            Row(Column("exp_others"),Column("exp_others_desc")), #TODO add unit
            HTML('<h3>Revenues</h3>'),
            Row("fun_feed4food",), #TODO add unit
            Row(Column("fun_others"),Column("fun_others_desc")), #TODO add unit  
            Row("rev_production",), #TODO add unit
            Row("rev_restaurant",), #TODO add unit
            Row("rev_events",), #TODO add unit
            Row(Column("rev_others"),Column("rev_others_desc")), #TODO add unit 
        )







