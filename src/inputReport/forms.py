from .models import InputReport, InputReportDetails, Input
from productionReport.models import Product, LLLocation, Garden
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML
from core import reportUtils


class InputReportForm(forms.ModelForm):
    class Meta:
        model = InputReport
        fields = ["city", "location", "garden", "application_date"]
        widgets = {
            "application_date": forms.DateInput(attrs={"type": "date"}),
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

        # self.fields['city'].widget.attrs.update({
        #     'id': 'id_city',
        #     'onchange': 'updateProductAndInputOptions()'
        # })

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
                Column("application_date"),
            ),
        )


class CustomSelect(Select):
    """
    Custom item list dropdown menu widget with options
    including unit data.
    """

    def __init__(self, *args, **kwargs):
        self.item_units = kwargs.pop("item_units", {})
        super().__init__(*args, **kwargs)

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        # see if its a function or a dictionary
        if value == "":
            option["attrs"]["disabled"] = "disabled"
        if callable(self.item_units):
            try:
                option["attrs"]["data-unit"] = self.item_units(value)
            except Exception as e:
                option["attrs"]["data-unit"] = ""
        elif value in self.item_units:
            option["attrs"]["data-unit"] = self.item_units[value]
        return option

class InputListForm(forms.ModelForm):
    class Meta:
        model = InputReportDetails
        fields = ["name_input", "name_product","area", "quantity"]

    name_product = forms.ChoiceField(
        label="Applied on ",
    )
    name_input = forms.ChoiceField(
        label="Input",
    )
    area = forms.FloatField(label="Application area size") 
    quantity = forms.FloatField(label="Quantity used")      

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "initial" in kwargs:
            initial = kwargs["initial"]
            self.fields["name_product"].initial = initial["name_product_id"]
            self.fields["area"].initial = initial["area"]
            initial_unit = Product.objects.get(name=initial["name_product_id"]).cultivation_type
            initial_unit_i = Input.objects.get(name=initial["name_input_id"]).unit
        else:
            initial_unit = ""
            initial_unit_i = ""
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        "name_input",
                        wrapper_class="d-flex align-items-center",
                        onchange="updateUnitInput(this)",
                        onload="updateUnitInput(this)",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field("quantity", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-2",
                ),
                Column(
                    HTML(f'<div class="unit-input-display"> {initial_unit_i} </div>'),
                    css_class="col-md-1",
                ),
                Column(
                    Field(
                        "name_product",
                        wrapper_class="d-flex align-items-center",
                        onchange="updateUnit(this)",
                        onload="updateUnit(this)",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field("area", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-2",
                ),
                Column(
                    HTML(f'<div class="unit-display"> {initial_unit} </div>'),
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
