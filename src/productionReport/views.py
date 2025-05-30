from .models import Product, ProductionReportDetails, ProduceReport
from .forms import ProduceReportForm, ProduceItemForm
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json


def get_post_report(request):
    if request.method == "GET":
        report = ProduceReportForm()
        item_form = ProduceItemForm()
        return render(
            request,
            "report_form.html",
            {
                "report_form": report,
                "item_form": item_form,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = ProduceReport.objects.create(
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            city=data.get("city"),
            location=data.get("location"),
            garden=data.get("garden"),
            user=request.user,
        )
        for post_item in data.get("items", []):
            itemObject = Product.objects.get(name=post_item.get("item_name"))
            ProductionReportDetails.objects.create(
                report_id=report,
                name=itemObject,
                quantity=post_item.get("quantity"),
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
