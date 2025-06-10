from django.shortcuts import render, get_object_or_404
from productionReport.models import Product, LLLocation, Garden
from inputReport.models import InputReport, InputReportDetails, Input
from inputReport.forms import InputReportForm, InputListForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def inputReport_list(request):
    reports = InputReport.objects.filter(user=request.user)
    return render(request, "inputReport_list.html", {"reports": reports})


def inputReport_details(request, report_id):
    report = InputReport.objects.get(report_id=report_id)
    items = Product.objects.all()
    inputs = Input.objects.all()
    return render(request, "inputReport_details.html", {"report": report, "items": items, "inputs": inputs})


def edit_report(request, report_id):
    report = get_object_or_404(InputReport, report_id=report_id)
    old_report_items = InputReportDetails.objects.filter(report_id=report_id)

    if request.method == "POST":
        data = json.loads(request.body)
        old_report_items.delete()
        for post_item in data.get("inputs", []):
            itemObject = Product.objects.get(name=post_item.get("name_product"))
            inputObject = Input.objects.get(name=post_item.get("name_input"))
            InputReportDetails.objects.create(
                report_id=report,
                name_product=itemObject,
                name_input=inputObject,
                quantity=post_item.get("quantity"),
                area=post_item.get("area"),
            )

        report.application_date = data.get("application_date")
        report.city = data.get("city")
        report.location = LLLocation.objects.get(name=data.get("location"))
        report.garden = Garden.objects.get(name=data.get("garden"))
        report.save()
        return JsonResponse({"redirect_url": reverse("inputReport_list")})

    if request.method == "GET":
        item_form_template = InputListForm()
        report_form = InputReportForm(instance=report)
        initial_data = []
        for item in old_report_items:
            initial_data.append({
                'name_product': item.name_product,
                'name_input': item.name_input,
                'area': item.area,
                'quantity': item.quantity,
            })
        formset = formset_factory(InputListForm, extra=0)(
            initial=initial_data
        )
        return render(
            request,
            "inputReport_edit.html",
            {
                "inputsApplied_form": item_form_template,
                "inputForm": report_form,
                "old_report_items": old_report_items,
                "formset": formset,
            },
        )
