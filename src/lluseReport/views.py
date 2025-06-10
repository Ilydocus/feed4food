from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import LLUseReport, LLUseReportPerUnderrepresentedGroups
from demographicReport.models import UnderrepresentedGroup
from .forms import LLUseGroupForm, LLUseReportForm
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json


def get_post_report(request):
    if request.method == "GET":
        report = LLUseReportForm()
        group_form = LLUseGroupForm()
        return render(
            request,
            "lluseReport.html",
            {
                "llUseForm": report,
                "llUseGroup_form": group_form,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = LLUseReport.objects.create(
            report_date=data.get("report_date"),
            city=data.get("city"),
            gardens_in_use=data.get("gardens_in_use"),
            total_ll_participants=data.get("total_ll_participants"),
            user=request.user,
        )
        for post_item in data.get("llUseGroupDetails", []):
            groupObject = UnderrepresentedGroup.objects.get(name=post_item.get("name"))
            LLUseReportPerUnderrepresentedGroups.objects.create(
                report_id=report,
                name=groupObject,
                ll_participants=post_item.get("ll_participants"),
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
