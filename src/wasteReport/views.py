from .models import WasteReportDetails, WasteReport, WasteType
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
            city=data.get("city"),
            location=data.get("location"),
            garden=data.get("garden"),
            user=request.user,
        )
        for post_action in data.get("actions", []):
            typeObject = WasteType.objects.get(name=post_action.get("wasteType"))
            WasteReportDetails.objects.create(
                report_id=report,
                wasteType=typeObject,
                quantity=post_action.get("quantity"),
                date=post_action.get("date"),
                wasteAction=post_action.get("wasteAction"),
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
