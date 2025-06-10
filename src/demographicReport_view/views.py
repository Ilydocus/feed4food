from django.shortcuts import render, get_object_or_404
from demographicReport.models import UnderrepresentedGroup, DemographicReport, DemographicReportPerUnderrepresentedGroups
from demographicReport.forms import DemographicGroupForm, DemographicReportForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def demographicReport_list(request):
    reports = DemographicReport.objects.filter(user=request.user)
    return render(request, "demographicReport_list.html", {"reports": reports})


def demographicReport_details(request, report_id):
    report = DemographicReport.objects.get(report_id=report_id)
    groups = UnderrepresentedGroup.objects.all()
    return render(request, "demographicReport_details.html", {"report": report, "groups": groups})


def edit_report(request, report_id):
    report = get_object_or_404(DemographicReport, report_id=report_id)
    old_report_items = DemographicReportPerUnderrepresentedGroups.objects.filter(report_id=report_id)

    if request.method == "POST":
        data = json.loads(request.body)
        old_report_items.delete()
        for post_item in data.get("demographicGroupDetails", []):
            groupObject = UnderrepresentedGroup.objects.get(name=post_item.get("name"))
            DemographicReportPerUnderrepresentedGroups.objects.create(
                report_id=report,
                name=groupObject,
                population=post_item.get("population"),
            )

        report.data_date = data.get("data_date")
        report.city = data.get("city")
        report.total_population = data.get("total_population")
        report.save()
        return JsonResponse({"redirect_url": reverse("demographicReport_list")})

    if request.method == "GET":
        item_form_template = DemographicGroupForm()
        report_form = DemographicReportForm(instance=report)
        initial_data = []
        for item in old_report_items:
            initial_data.append({
                'name': item.name,
                'population': item.population,
            })
        formset = formset_factory(DemographicGroupForm, extra=0)(
            initial=initial_data
        )
        return render(
            request,
            "demographicReport_edit.html",
            {
                "demographicGroup_form": item_form_template,
                "demographicForm": report_form,
                "old_report_items": old_report_items,
                "formset": formset,
            },
        )
