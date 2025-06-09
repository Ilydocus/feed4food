from django.shortcuts import render, get_object_or_404
from productionReport.models import LLLocation, Garden
from wasteReport.models import WasteReport, WasteReportDetails, WasteType
from wasteReport.forms import WasteActionForm, WasteReportForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def wasteReport_list(request):
    reports = WasteReport.objects.filter(user=request.user)
    return render(request, "wasteReport_list.html", {"reports": reports})


def wasteReport_details(request, report_id):
    report = WasteReport.objects.get(report_id=report_id)
    types = WasteType.objects.all()
    return render(request, "wasteReport_details.html", {"report": report, "types": types})


def edit_report(request, report_id):
    report = get_object_or_404(WasteReport, report_id=report_id)
    old_report_items = WasteReportDetails.objects.filter(report_id=report_id)

    if request.method == "POST":
        data = json.loads(request.body)
        old_report_items.delete()
        for post_item in data.get("actions", []):
            typeObject = WasteType.objects.get(name=post_item.get("wasteType"))
            WasteReportDetails.objects.create(
                report_id=report,
                wasteType=typeObject,
                wasteAction = post_item.get("wasteAction"),
                date=post_item.get("date"),
                quantity=post_item.get("quantity"),
            )

        report.city = data.get("city")
        report.location = LLLocation.objects.get(name=data.get("location"))
        report.garden = Garden.objects.get(name=data.get("garden"))
        report.save()
        return JsonResponse({"redirect_url": reverse("wasteReport_list")})

    if request.method == "GET":
        action_form_template = WasteActionForm()
        report_form = WasteReportForm(instance=report)
        formset = formset_factory(WasteActionForm, extra=0)(
            initial=old_report_items.values()
        )
        return render(
            request,
            "wasteReport_edit.html",
            {
                "action_form": action_form_template,
                "waste_form": report_form,
                "old_report_items": old_report_items,
                "formset": formset,
            },
        )
