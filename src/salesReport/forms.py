from .models import SalesReport, SalesReportDetails
from productionReport.models import Product, LLLocation, Garden
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

# class CustomSelect(Select):
#     """
#     Custom item list dropdown menu widget with options
#     including unit data.
#     """

#     def __init__(self, *args, **kwargs):
#         self.item_units = kwargs.pop("item_units", {})
#         super().__init__(*args, **kwargs)

#     def create_option(
#         self, name, value, label, selected, index, subindex=None, attrs=None
#     ):
#         option = super().create_option(
#             name, value, label, selected, index, subindex=subindex, attrs=attrs
#         )
#         # see if its a function or a dictionary
#         if value == "":
#             option["attrs"]["disabled"] = "disabled"
#         if callable(self.item_units):
#             try:
#                 option["attrs"]["data-unit"] = self.item_units(value)
#             except Exception as e:
#                 option["attrs"]["data-unit"] = ""
#         elif value in self.item_units:
#             option["attrs"]["data-unit"] = self.item_units[value]
#         return option


class SalesActionForm(forms.ModelForm):
    class Meta:
        model = SalesReportDetails
        fields = ["sale_date", "sale_location", "product", "price", "quantity"]
        widgets = {
           "sale_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels ={
            'product':'Product ',
        }

    location = forms.CharField(label="Sale location")

    # what = forms.ChoiceField(
    #     label="Product",
    # )
    quantity = forms.FloatField(label="Quantity")
    price = forms.FloatField(label="Price")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if "initial" in kwargs:
        #     initial = kwargs["initial"]
        #     self.fields["what"].initial = initial["name_id"]
        #     self.fields["quantity"].initial = initial["quantity"]
        #     self.fields["currency"].initial = initial["currency"]
        #     initial_unit = Product.objects.get(name=initial["name_id"]).unit
        # else:
        # Add CSS class for JavaScript targeting
        self.fields['product'].widget.attrs.update({
            'class': 'product-name-select'
        })

        initial_unit = ""
        initial_unit2 = ""
        initial_currency = ""
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
                    css_class="col-md-2",
                ),
                Column(
                    Field(
                        "sale_location",
                        wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field(
                        "product",
                        wrapper_class="d-flex align-items-center",
                        onchange="updateUnitAndCurrency(this)",
                        onload="updateUnitAndCurrency(this)",
                    ),
                    css_class="col-md-2",
                ),
                Column(
                    Field("quantity", wrapper_class="d-flex align-items-center"),
                    css_class="col-md-2",
                ),
                Column(
                    HTML(f'<div class="unit-display"> {initial_unit} </div>'),
                    css_class="col-md-1",
                ),
                Column(
                    Field("price", wrapper_class="d-flex align-items-center",
                    ),
                    css_class="col-md-2",
                ),
                Column(
                    HTML(f'<div class="unitandcurrency-display"> {initial_currency} per {initial_unit2}</div>'),
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






