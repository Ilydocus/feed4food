from .models import EventReport, EventPersonDetails, UnderrepresentedGroup, EventParticipantDetails
from .forms import EventReportForm, EventPersonDetailsForm, EventParticipantDetailsForm
from core import reportUtils
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json


def get_post_report(request):
    if request.method == "GET":
        report = EventReportForm()
        personDetails_form = EventPersonDetailsForm()
        participantDetails_form = EventParticipantDetailsForm()
        return render(
            request,
            "eventForm.html",
            {
                "event_form": report,
                "eventGroupList_form": personDetails_form,
                "eventParticipantList_form": participantDetails_form,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = EventReport.objects.create(
            city=data.get("city"),
            user=request.user,
            currency=data.get("currency"),
            event_date=data.get("event_date"),
            event_name=data.get("event_name"),
            event_loc=data.get("event_loc"),
            event_type=data.get("event_type"),
            event_desc=data.get("event_desc"),
            event_costs=data.get("event_costs"),
            event_costs_desc=data.get("event_costs_desc"),
            event_revenues=data.get("event_revenues"),
            event_revenues_desc=data.get("event_revenues_desc"),
            total_invited=data.get("total_invited"),
            total_participants=data.get("total_participants"),
        )
        for post_group in data.get("eventGroupDetails", []):
            groupObject = UnderrepresentedGroup.objects.get(pk=post_group.get("name"))
            EventPersonDetails.objects.create(
                report_id=report,
                name=groupObject,
                number_invited=post_group.get("number_invited"),
                number_participant=post_group.get("number_participant"),
            )
        for post_group in data.get("eventParticipantDetails", []):
                    group_value = post_group.get("group")
                    if group_value:
                        groupObject = UnderrepresentedGroup.objects.get(pk=group_value)
                    else:
                        groupObject = None
                    EventParticipantDetails.objects.create(
                        report_id=report,
                        participant_id=post_group.get("participant_id"),
                        group=groupObject,
                        test_result=post_group.get("test_result"),
                        event_grade=post_group.get("event_grade"),
                    )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
