from django.shortcuts import render, get_object_or_404
from demographicReport.models import UnderrepresentedGroup
from eventReport.models import EventReport, EventPersonDetails, EventParticipantDetails
from eventReport.forms import EventReportForm, EventPersonDetailsForm, EventParticipantDetailsForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def eventReport_list(request):
    reports = EventReport.objects.filter(user=request.user)
    return render(request, "eventReport_list.html", {"reports": reports})


def eventReport_details(request, report_id):
    report = EventReport.objects.get(report_id=report_id)
    groups = UnderrepresentedGroup.objects.all()
    return render(request, "eventReport_details.html", {"report": report, "groups": groups})


def edit_report(request, report_id):
    report = get_object_or_404(EventReport, report_id=report_id)
    old_report_items = EventPersonDetails.objects.filter(report_id=report_id)
    old_report_participants_items = EventParticipantDetails.objects.filter(report_id=report_id)

    if request.method == "POST":
        data = json.loads(request.body)
        old_report_items.delete()
        for post_item in data.get("eventGroupDetails", []):
            groupObject = UnderrepresentedGroup.objects.get(pk=post_item.get("name"))
            EventPersonDetails.objects.create(
                report_id=report,
                name=groupObject,
                number_invited=post_item.get("number_invited"),
                number_participant=post_item.get("number_participant"),
            )
        old_report_participants_items.delete()
        for post_item in data.get("eventParticipantDetails", []):
            group_value = post_item.get("group")
            groupObject = UnderrepresentedGroup.objects.get(pk=group_value) if group_value else None
            EventParticipantDetails.objects.create(
                report_id=report,
                group=groupObject,
                participant_id=post_item.get("participant_id"),
                test_result=post_item.get("test_result"),
                event_grade=post_item.get("event_grade"),
            )

        report.event_date = data.get("event_date")
        report.event_name = data.get("event_name")
        report.event_loc = data.get("event_loc")
        report.event_type = data.get("event_type")
        report.event_desc = data.get("event_desc")
        report.city = data.get("city")
        report.total_invited = data.get("total_invited")
        report.total_participants = data.get("total_participants")
        report.currency = data.get("currency")
        report.event_costs = data.get("event_costs")
        report.event_costs_desc = data.get("event_costs_desc")
        report.event_revenues = data.get("event_revenues")
        report.event_revenues_desc = data.get("event_revenues_desc")
        report.save()
        return JsonResponse({"redirect_url": reverse("eventReport_list")})

    if request.method == "GET":
        item_form_template = EventPersonDetailsForm()
        participant_form_template = EventParticipantDetailsForm()
        report_form = EventReportForm(instance=report)
        initial_data = []
        for item in old_report_items:
            initial_data.append({
                'name': item.name,
                'number_invited': item.number_invited,
                'number_participant': item.number_participant,
            })
        initial_data2 = []
        for item in old_report_participants_items:
            initial_data2.append({
                'participant_id': item.participant_id,
                'group': item.group,
                'test_result': item.test_result,
                'event_grade': item.event_grade,
            })
        formset = formset_factory(EventPersonDetailsForm, extra=0)(
            initial=initial_data
        )
        formset2 = formset_factory(EventParticipantDetailsForm, extra=0)(
                    initial=initial_data2
                )
        return render(
            request,
            "eventReport_edit.html",
            {
                "eventGroupList_form": item_form_template,
                "eventParticipantList_form": participant_form_template,
                "event_form": report_form,
                "old_report_items": old_report_items,
                "old_report_participants_items": old_report_participants_items,
                "formset": formset,
                "formset2": formset2,
            },
        )
