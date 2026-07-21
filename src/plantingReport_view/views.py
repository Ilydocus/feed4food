from django.shortcuts import render, get_object_or_404
from plantingReport.models import PlantingReport, PlantingReportDetails
from productionReport.models import Product, LLLocation, Garden
from plantingReport.forms import PlantingProductForm, PlantingReportForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def plantingReport_list(request):
    reports = PlantingReport.objects.filter(user=request.user)
    return render(request, "plantingReport_list.html", {"reports": reports})

#TODO: not sure the below is used
def plantingReport_details(request, report_id):
    report = PlantingReport.objects.get(report_id=report_id)
    items = Product.objects.all()
    return render(request, "plantingReport_details.html", {"report": report, "items": items})


def edit_report(request, report_id):
    report = get_object_or_404(PlantingReport, report_id=report_id)
    old_report_items = PlantingReportDetails.objects.filter(report_id=report_id)

    if request.method == "POST":
        data = json.loads(request.body)
        old_report_items.delete()
        for post_item in data.get("items", []):
            itemObject = Product.objects.get(name=post_item.get("name"))
            PlantingReportDetails.objects.create(
                report_id=report,
                name=itemObject,
                area_quantity_planted=post_item.get("area_quantity_planted"),
                planting_unit=post_item.get("planting_unit"),
            )

        report.planting_date = data.get("planting_date")
        report.city = data.get("city")
        report.location = LLLocation.objects.get(name=data.get("location"))
        report.garden = Garden.objects.get(name=data.get("garden"))
        report.save()
        return JsonResponse({"redirect_url": reverse("plantingReport_list")})

    if request.method == "GET":
        item_form_template = PlantingProductForm()
        report_form = PlantingReportForm(instance=report)
        initial_data = []
        for item in old_report_items:
            initial_data.append({
                'name': item.name,
                'area_quantity_planted': item.area_quantity_planted,
                'planting_unit': item.planting_unit,
            })
        formset = formset_factory(PlantingProductForm, extra=0)(
            initial=initial_data
        )
        return render(
            request,
            "plantingReport_edit.html",
            {
                "productPlanted_form": item_form_template,
                "plantingReport_form": report_form,
                "old_report_items": old_report_items,
                "formset": formset,
            },
        )
