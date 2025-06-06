from .models import CultivationReportDetails, CultivationReport
from productionReport.models import Product
from .forms import CultivationReportForm, CultivationProductForm
from django.shortcuts import render

from django.urls import reverse
from django.http import JsonResponse
import json

def get_post_report(request):
    if request.method == "GET":
        report = CultivationReportForm()
        item_form = CultivationProductForm()
        return render(
            request,
            "cultivationReport.html",
            {
                "cultivationReport_form": report,
                "productCultivated_form": item_form,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = CultivationReport.objects.create(
            cultivation_date=data.get("cultivation_date"),
            city=data.get("city"),
            location=data.get("location"),
            garden=data.get("garden"),
            user=request.user,
        )
        for post_item in data.get("items", []):
            itemObject = Product.objects.get(name=post_item.get("name"))
            CultivationReportDetails.objects.create(
                report_id=report,
                name=itemObject,
                area_cultivated=post_item.get("area_cultivated"),
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

