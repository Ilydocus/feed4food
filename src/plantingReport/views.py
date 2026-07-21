from .models import PlantingReportDetails, PlantingReport
from productionReport.models import Product, LLLocation, Garden
from .forms import PlantingReportForm, PlantingProductForm
from django.shortcuts import render

from django.urls import reverse
from django.http import JsonResponse
import json

def get_post_report(request):
    if request.method == "GET":
        report = PlantingReportForm()
        item_form = PlantingProductForm()
        return render(
            request,
            "plantingReport.html",
            {
                "plantingReport_form": report,
                "productPlanted_form": item_form,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = PlantingReport.objects.create(
            planting_date=data.get("planting_date"),
            city=data.get("city"),
            location=LLLocation.objects.get(name=data.get("location")),
            garden=Garden.objects.get(name=data.get("garden")),
            user=request.user,
        )
        for post_item in data.get("items", []):
            itemObject = Product.objects.get(name=post_item.get("name"))
            PlantingReportDetails.objects.create(
                report_id=report,
                name=itemObject,
                area_quantity_planted=post_item.get("area_quantity_planted"),
                planting_unit=post_item.get("planting_unit"), #TODO see if need to use a similar way as product
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

