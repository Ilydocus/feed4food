from .models import FinancialReport
from .forms import FinancialReportForm
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json


def get_post_report(request):
    if request.method == "GET":
        report = FinancialReportForm()
        return render(
            request,
            "financialForm.html",
            {
                "financialForm": report,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = FinancialReport.objects.create(
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            city=data.get("city"),
            location=data.get("location"),
            garden=data.get("garden"),
            user=request.user,
            #TODO: add the other fields or not needed?
        )
        # for post_item in data.get("items", []):
        #     itemObject = Item.objects.get(name=post_item.get("item_name"))
        #     ProduceReportDetails.objects.create(
        #         report_id=report,
        #         name=itemObject,
        #         quantity=post_item.get("quantity"),
        #     )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)#

