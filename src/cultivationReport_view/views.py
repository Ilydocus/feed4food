from django.shortcuts import render, get_object_or_404
from cultivationReport.models import CultivationReport, CultivationReportDetails
from productionReport.models import Product, LLLocation, Garden
from cultivationReport.forms import CultivationProductForm, CultivationReportForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def cultivationReport_list(request):
    reports = CultivationReport.objects.filter(user=request.user)
    return render(request, "cultivationReport_list.html", {"reports": reports})

#TODO: not sure the below is used
def cultivationReport_details(request, report_id):
    report = CultivationReport.objects.get(report_id=report_id)
    items = Product.objects.all()
    return render(request, "cultivationReport_details.html", {"report": report, "items": items})


def edit_report(request, report_id):
    report = get_object_or_404(CultivationReport, report_id=report_id)
    old_report_items = CultivationReportDetails.objects.filter(report_id=report_id)

    if request.method == "POST":
        data = json.loads(request.body)
        old_report_items.delete()
        for post_item in data.get("items", []):
            itemObject = Product.objects.get(name=post_item.get("name"))
            CultivationReportDetails.objects.create(
                report_id=report,
                name=itemObject,
                area_cultivated=post_item.get("area_cultivated"),
            )

        report.cultivation_date = data.get("cultivation_date")
        report.city = data.get("city")
        report.location = LLLocation.objects.get(name=data.get("location"))
        report.garden = Garden.objects.get(name=data.get("garden"))
        report.save()
        return JsonResponse({"redirect_url": reverse("cultivationReport_list")})

    if request.method == "GET":
        item_form_template = CultivationProductForm()
        report_form = CultivationReportForm(instance=report)
        initial_data = []
        for item in old_report_items:
            initial_data.append({
                'name': item.name,
                'area_cultivated': item.area_cultivated,
            })
        formset = formset_factory(CultivationProductForm, extra=0)(
            initial=initial_data
        )
        return render(
            request,
            "cultivationReport_edit.html",
            {
                "productCultivated_form": item_form_template,
                "cultivationReport_form": report_form,
                "old_report_items": old_report_items,
                "formset": formset,
            },
        )
