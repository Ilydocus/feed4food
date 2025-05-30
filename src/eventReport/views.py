from .models import EventReport, EventPersonDetails, UnderrepresentedGroups
from .forms import EventReportForm, EventPersonForm, EventPersonDetailsForm
from core import reportUtils
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json


def get_post_report(request):
    if request.method == "GET":
        report = EventReportForm()
        person_form = EventPersonForm()
        personDetails_form = EventPersonDetailsForm()
        return render(
            request,
            "eventForm.html",
            {
                "event_form": report,
                "eventPerson_form": person_form,
                "eventGroupList_form": personDetails_form,
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
            groupObject = UnderrepresentedGroups.objects.get(name=post_group.get("name"))
            EventPersonDetails.objects.create(
                report_id=report,
                name=groupObject,
                number_invited=post_group.get("number_invited"),
                number_participant=post_group.get("number_participant"),
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
