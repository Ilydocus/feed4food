from .models import WasteReportDetails, WasteReport, WasteType
from .forms import WasteReportForm, WasteActionForm
from productionReport.models import LLLocation, Garden
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
            location=LLLocation.objects.get(name=data.get("location")),
            garden=Garden.objects.get(name=data.get("garden")),
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
    
def get_wastetypes_by_city(request):
    """
    AJAX view to get waste types filtered by city
    """
    city_id = request.GET.get('city_id')
    
    if city_id:
        try:
            types = WasteType.objects.filter(living_lab=city_id).values('name', 'unit')
            type_list = list(types)
        except:
            type_list = []
    else:
        type_list = []
    
    return JsonResponse({'types': type_list})
