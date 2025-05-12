from .models import WasteReport, WasteReportDetails, WasteAction, WasteType
from django import forms
from django.forms.widgets import Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Button, Field, HTML


class WasteReportForm(forms.ModelForm):
    class Meta:
        model = WasteReport
        fields = ["start_date", "end_date", "city", "location", "garden"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

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
                Column("start_date"),
                Column("end_date"),
            ),
        )

class CustomSelectType(Select):
    """
    Custom action list dropdown menu widget with options including unit
    """

    def __init__(self, *args, **kwargs):
        self.type_units = kwargs.pop("type_units", {})
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
        if callable(self.type_units):
            try:
                option["attrs"]["data-unit"] = self.type_units(value)
            except Exception as e:
                option["attrs"]["data-unit"] = ""
        elif value in self.type_units:
            option["attrs"]["data-unit"] = self.type_units[value]
        return option

class CustomSelectAction(Select):
    """
    Custom action list dropdown menu widget with options 
    """

    def __init__(self, *args, **kwargs):
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
        return option


def get_wasteAction_choices():
    try:
        WASTEACTION_CHOICES = [
            (waction, waction) for waction in WasteAction.objects.values_list("name", flat=True)
        ]
        WASTEACTION_CHOICES.insert(0, ("", "Select action"))
    except Exception as e:
        WASTEACTION_CHOICES = [("", "Error fetching the actions")]
    return WASTEACTION_CHOICES

def get_wasteType_choices():
    try:
        WASTETYPE_CHOICES = [
            (wtype, wtype) for wtype in WasteType.objects.values_list("name", flat=True)
        ]
        WASTETYPE_CHOICES.insert(0, ("", "Select waste type"))
    except Exception as e:
        WASTETYPE_CHOICES = [("", "Error fetching the types")]
    return WASTETYPE_CHOICES

def get_wasteType_units(value):
    try:
        WASTETYPE_UNITS = {
            wtype: unit for (wtype, unit) in WasteType.objects.values_list("name", "unit")
        }
        return WASTETYPE_UNITS[value]
    except Exception as e:
        WASTETYPE_UNITS = {}
        return ""


class WasteActionForm(forms.ModelForm):
    class Meta:
        model = WasteReportDetails
        fields = ["wasteAction", "wasteType", "quantity"]

    wasteAction = forms.ChoiceField(
        choices=get_wasteAction_choices,
        label="Action",
        widget=CustomSelectAction(), #TODO remove the need for the argument
    )
    wasteType = forms.ChoiceField(
        choices=get_wasteType_choices,
        label="Type",
        widget=CustomSelectType(type_units=get_wasteType_units),
    )
    quantity = forms.FloatField(label="Quantity")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "initial" in kwargs:
            initial = kwargs["initial"]
            self.fields["wasteAction"].initial = initial["name_id"]
            self.fields["wasteType"].initial = initial["name_id"]
            self.fields["quantity"].initial = initial["quantity"]
            initial_unit = WasteType.objects.get(name=initial["name_id"]).unit
        else:
            initial_unit = ""
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        "wasteAction",
                        wrapper_class="d-flex align-items-center",
                        #onchange="updateUnit(this)",
                        #onload="updateUnit(this)",
                    ),
                    css_class="col-md-3",
                ),
                Column(
                    Field(
                        "wasteType",
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






