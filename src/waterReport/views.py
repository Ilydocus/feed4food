from .models import WaterReport, WaterReportIrrigation, WaterReportRainfall
from .forms import WaterReportForm, WaterIrrigationForm, WaterRainfallForm
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json


def get_post_report(request):
    if request.method == "GET":
        report = WaterReportForm()
        rainfall_form = WaterRainfallForm()
        irrigation_form = WaterIrrigationForm()
        return render(
            request,
            "waterForm.html",
            {
                "water_form": report,
                "rainfall_form": rainfall_form,
                "irrigation_form": irrigation_form,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = WaterReport.objects.create(
            
            city=data.get("city"),
            location=data.get("location"),
            garden=data.get("garden"),
            user=request.user,
        )
        for post_action in data.get("rainfalls", []):
            WaterReportRainfall.objects.create(
                report_id=report,
                quantity=post_action.get("quantity"),
                start_date=data.get("start_date"),
                end_date=data.get("end_date"),
            )
        for post_action in data.get("irrigations", []):
            WaterReportIrrigation.objects.create(
                report_id=report,
                quantity=post_action.get("quantity"),
                start_date=data.get("start_date"),
                end_date=data.get("end_date"),
                period=data.get("period"),
                frequency_times=data.get("frequency_times"),
                frequency_interval=data.get("frequency_interval"),
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

