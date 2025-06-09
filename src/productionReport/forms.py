from .models import Product, LLLocation, Garden, ProductionReport, ProductionReportDetails
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML


class ProductionReportForm(forms.ModelForm):
    class Meta:
        model = ProductionReport
        fields = ["city", "location", "garden", "production_date"]
        widgets = {
            "production_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = LLLocation.objects.none()
        self.fields['garden'].queryset = Garden.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['location'].queryset = LLLocation.objects.filter(living_lab_id=city_id).order_by('name')#TODO is this used because the field does not exist!
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
                Column("production_date"),
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


class ProductionProductForm(forms.ModelForm):
    class Meta:
        model = ProductionReportDetails
        fields = ["item", "quantity"]

    item = forms.ChoiceField(
        label="Product",
    )
    quantity = forms.IntegerField(label="Quantity")    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "initial" in kwargs:
            initial = kwargs["initial"]
            self.fields["item"].initial = initial["name_id"]
            self.fields["quantity"].initial = initial["quantity"]
            initial_unit = Product.objects.get(name=initial["name_id"]).unit
        else:
            initial_unit = ""
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        "item",
                        wrapper_class="d-flex align-items-center",
                        onchange="updateUnit(this)",
                        onload="updateUnit(this)",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field("quantity", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
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
