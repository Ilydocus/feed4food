from django.shortcuts import render, get_object_or_404
from waterReport.models import WaterReport, WaterReportIrrigation, WaterReportRainfall
from productionReport.models import LLLocation, Garden
from waterReport.forms import WaterReportForm, WaterRainfallForm, WaterIrrigationForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def waterReport_list(request):
    reports = WaterReport.objects.filter(user=request.user)
    return render(request, "waterReport_list.html", {"reports": reports})

#OBS modified
def waterReport_details(request, report_id):
    report = WaterReport.objects.get(report_id=report_id)
    return render(request, "waterReport_details.html", {"report": report})


def edit_report(request, report_id):
    report = get_object_or_404(WaterReport, report_id=report_id)
    old_report_items_r = WaterReportRainfall.objects.filter(report_id=report_id)
    old_report_items_i = WaterReportIrrigation.objects.filter(report_id=report_id)

    if request.method == "POST":
        data = json.loads(request.body)
        old_report_items_r.delete()
        old_report_items_i.delete()
        for post_item in data.get("rainfalls", []):
            WaterReportRainfall.objects.create(
                report_id=report,
                start_date=post_item.get("start_date"),
                end_date=post_item.get("end_date"),
                quantity=post_item.get("quantity"),
            )
        for post_item in data.get("irrigations", []):
            WaterReportIrrigation.objects.create(
                report_id=report,
                start_date=post_item.get("start_date"),
                end_date=post_item.get("end_date"),
                period=post_item.get("period"),
                frequency_times=post_item.get("frequency_times"),
                frequency_interval=post_item.get("frequency_interval"),
                quantity=post_item.get("quantity"),
            )

        report.city = data.get("city")
        report.location = LLLocation.objects.get(name=data.get("location"))
        report.garden = Garden.objects.get(name=data.get("garden"))
        report.save()
        return JsonResponse({"redirect_url": reverse("waterReport_list")})

    if request.method == "GET":
        rainfall_form_template = WaterRainfallForm()
        irrigation_form_template = WaterIrrigationForm()
        report_form = WaterReportForm(instance=report)
        formset_r = formset_factory(WaterRainfallForm, extra=0)(
            initial=old_report_items_r.values()
        )
        formset_i = formset_factory(WaterIrrigationForm, extra=0)(
            initial=old_report_items_i.values()
        )
        return render(
            request,
            "waterReport_edit.html",
            {
                "rainfall_form": rainfall_form_template,
                "irrigation_form": irrigation_form_template,
                "water_form": report_form,
                "old_report_items_r": old_report_items_r,
                "old_report_items_i": old_report_items_i,
                "formset_r": formset_r,
                "formset_i": formset_i,
            },
        )
