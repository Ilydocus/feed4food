from .models import CultivationReport, CultivationReportDetails
from productionReport.models import Product, LLLocation, Garden
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML


class CultivationReportForm(forms.ModelForm):
    class Meta:
        model = CultivationReport
        fields = ["city", "location", "garden", "cultivation_date"]
        widgets = {
            "cultivation_date": forms.DateInput(attrs={"type": "date"}),
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
                Column("cultivation_date"),
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



def get_item_choices():
    try:
        ITEM_CHOICES = [
            (item, item) for item in Product.objects.values_list("name", flat=True)
        ]
        ITEM_CHOICES.insert(0, ("", "Select Product"))
    except Exception as e:
        ITEM_CHOICES = [("", "Select Product")]
    return ITEM_CHOICES


def get_item_units_cultivation(value):
    try:
        ITEM_UNITS = {
            item: unit for (item, unit) in Product.objects.values_list("name", "cultivation_type")
        }
        return ITEM_UNITS[value]
    except Exception as e:
        ITEM_UNITS = {}
        return ""


class CultivationProductForm(forms.ModelForm):
    class Meta:
        model = CultivationReportDetails
        fields = ["name", "area_cultivated"]

    name = forms.ChoiceField(
        choices=get_item_choices,
        label="Product",
        widget=CustomSelect(item_units=get_item_units_cultivation),
    )
    area_cultivated = forms.IntegerField(label="Area cultivated")    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "initial" in kwargs:
            initial = kwargs["initial"]
            self.fields["name"].initial = initial["name_id"]
            self.fields["area_cultivated"].initial = initial["area_cultivated"]
            initial_unit = Product.objects.get(name=initial["name_id"]).cultivation_type
        else:
            initial_unit = ""
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        "name",
                        wrapper_class="d-flex align-items-center",
                        onchange="updateUnitCultivation(this)",
                        onload="updateUnitCultivation(this)",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field("area_cultivated", wrapper_class="d-flex align-items-center"),
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
