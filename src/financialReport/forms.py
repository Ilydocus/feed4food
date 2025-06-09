from .models import FinancialReport
from productionReport.models import LLLocation, Garden
from core import reportUtils
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML
import datetime

class FinancialReportForm(forms.ModelForm):
    class Meta:
        model = FinancialReport
        fields = ["month", "year", "currency", "city", "location", "garden", "exp_workforce", 
        "exp_purchase", "exp_others", "exp_others_desc", "fun_feed4food", "fun_others", "fun_others_desc", 
        "rev_restaurant", "rev_others", "rev_others_desc"]
        widgets = {
            #"start_date": forms.DateInput(attrs={"type": "date"}),
            #"end_date": forms.DateInput(attrs={"type": "date"}),
        }
    YEAR_CHOICES = [(year, year) for year in range(2024, datetime.datetime.now().year+1)]

    month = forms.ChoiceField(choices=reportUtils.Months, widget=forms.Select)
    year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select)

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

        self.fields['exp_workforce'].label = "Workforce costs"
        self.fields['exp_purchase'].label = "Purchase costs"
        self.fields['exp_others'].label = "Other costs"
        self.fields['exp_others_desc'].label = "Short description"
        self.fields['fun_feed4food'].label = "FEED4FOOD funding"
        self.fields['fun_others'].label = "Other funding"
        self.fields['fun_others_desc'].label = "Short description"
        self.fields['rev_restaurant'].label = "Sales in restaurant"
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
                Column("month"),
                Column("year"),
            ),
            Row(
                Column(Field("currency"),
                onchange="updateCurrency(this)",
                onload="updateCurrency(this)",
                ),
            ),
            HTML('<h3>Expenses</h3>'),
            Row(Column(Field("exp_workforce"),),
            ), 
            Row("exp_purchase",), #TODO add unit
            Row(Column("exp_others"),Column("exp_others_desc")), #TODO add unit
            HTML('<h3>Revenues</h3>'),
            Row("fun_feed4food",), #TODO add unit
            Row(Column("fun_others"),Column("fun_others_desc")), #TODO add unit
            HTML('<div class="p1">Production sales are reported using the sales report</div>'),  
            Row("rev_production",), #TODO add unit
            Row("rev_restaurant",), #TODO add unit
            HTML('<div class="p1">Revenues from event are reported using the event report</div>'),  
            Row(Column("rev_others"),Column("rev_others_desc")), #TODO add unit 
        )







