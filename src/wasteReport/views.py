from .models import WasteReportDetails, WasteReport
from .forms import WasteReportForm, WasteActionForm
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json


def get_post_report(request):
    if request.method == "GET":
        report = WasteReportForm()
        action_form = WasteActionForm()
        return render(
            request,
            "wasteForm.html",
            {
                "waste_form": report,
                "action_form": action_form,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = WasteReport.objects.create(
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            city=data.get("city"),
            location=data.get("location"),
            garden=data.get("garden"),
            user=request.user,
        )
        for post_action in data.get("actions", []):
            actionObject = Action.objects.get(name=post_action.get("action_name"))
            WasteReportDetails.objects.create(
                report_id=report,
                name=actionObject,
                quantity=post_action.get("quantity"),
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
