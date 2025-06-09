from django.shortcuts import render, get_object_or_404
from lluseReport.models import LLUseReport, LLUseReportPerUnderrepresentedGroups
from demographicReport.models import UnderrepresentedGroup
from lluseReport.forms import LLUseGroupForm, LLUseReportForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def lluseReport_list(request):
    reports = LLUseReport.objects.filter(user=request.user)
    return render(request, "lluseReport_list.html", {"reports": reports})


def lluseReport_details(request, report_id):
    report = LLUseReport.objects.get(report_id=report_id)
    groups = UnderrepresentedGroup.objects.all()
    return render(request, "lluseReport_details.html", {"report": report, "groups": groups})


def edit_report(request, report_id):
    report = get_object_or_404(LLUseReport, report_id=report_id)
    old_report_items = LLUseReportPerUnderrepresentedGroups.objects.filter(report_id=report_id)

    if request.method == "POST":
        data = json.loads(request.body)
        old_report_items.delete()
        for post_item in data.get("llUseGroupDetails", []):
            groupObject = UnderrepresentedGroup.objects.get(name=post_item.get("name"))
            LLUseReportPerUnderrepresentedGroups.objects.create(
                report_id=report,
                name=groupObject,
                ll_participants=post_item.get("ll_participants"),
            )

        report.report_date = data.get("report_date")
        report.city = data.get("city")
        report.total_ll_participants = data.get("total_ll_participants")
        report.gardens_in_use = data.get("gardens_in_use")
        report.save()
        return JsonResponse({"redirect_url": reverse("lluseReport_list")})

    if request.method == "GET":
        item_form_template = LLUseGroupForm()
        report_form = LLUseReportForm(instance=report)
        initial_data = []
        for item in old_report_items:
            initial_data.append({
                'name': item.name,
                'll_participants': item.ll_participants,
            })
        formset = formset_factory(LLUseGroupForm, extra=0)(
            initial=initial_data
        )
        return render(
            request,
            "lluseReport_edit.html",
            {
                "llUseGroup_form": item_form_template,
                "llUseForm": report_form,
                "old_report_items": old_report_items,
                "formset": formset,
            },
        )
