from .models import SalesReport, SalesReportDetails
from report.models import Item
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML


class SalesReportForm(forms.ModelForm):
    class Meta:
        model = SalesReport
        fields = ["city", "location", "garden", "currency"]

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
            Row(
                Column(
                    Field("currency", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-3",
                ),
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
            (item, item) for item in Item.objects.values_list("name", flat=True)
        ]
        ITEM_CHOICES.insert(0, ("", "Select Item"))
    except Exception as e:
        ITEM_CHOICES = [("", "Select Item")]
    return ITEM_CHOICES


def get_item_units(value):
    try:
        ITEM_UNITS = {
            item: unit for (item, unit) in Item.objects.values_list("name", "unit")
        }
        return ITEM_UNITS[value]
    except Exception as e:
        ITEM_UNITS = {}
        return ""


class SalesActionForm(forms.ModelForm):
    class Meta:
        model = SalesReportDetails
        fields = ["sale_date", "location", "what", "price", "quantity"]
        widgets = {
            "sale_date": forms.DateInput(attrs={"type": "date"}),
        }

    location = forms.CharField(label="Sale location")

    what = forms.ChoiceField(
        choices=get_item_choices,
        label="Product",
        widget=CustomSelect(item_units=get_item_units),
    )
    quantity = forms.FloatField(label="Quantity")
    price = forms.FloatField(label="Price")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "initial" in kwargs:
            initial = kwargs["initial"]
            self.fields["what"].initial = initial["name_id"]
            self.fields["quantity"].initial = initial["quantity"]
            self.fields["currency"].initial = initial["currency"]
            initial_unit = Item.objects.get(name=initial["name_id"]).unit
        else:
            initial_unit = ""
            initial_unit2 = "product unit"
            initial_currency = "selected currency"
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        "sale_date",
                        wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field(
                        "location",
                        wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field(
                        "what",
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
                    Field("price", wrapper_class="d-flex align-items-center",
                    onchange="getCurrency(this)",
                    onload="getCurrency(this)",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    HTML(f'<div class="currency-display"> {initial_currency} </div>'),
                    HTML(f' per'),
                    HTML(f'<div class="unit-display2"> {initial_unit2} </div>'),
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






