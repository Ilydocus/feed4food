from .models import SalesReportDetails, SalesReport
from report.models import Product
from .forms import SalesReportForm, SalesActionForm
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json


def get_post_report(request):
    if request.method == "GET":
        report = SalesReportForm()
        item_form = SalesActionForm()
        return render(
            request,
            "salesForm.html",
            {
                "sales_form": report,
                "salesList_form": item_form,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = SalesReport.objects.create(
            city=data.get("city"),
            location=data.get("location"),
            garden=data.get("garden"),
            user=request.user,
            currency=data.get("currency"),
        )
        for post_item in data.get("salesActions", []):
            itemObject = Product.objects.get(name=post_item.get("product"))
            SalesReportDetails.objects.create(
                sale_date=post_item.get("sale_date"),
                report_id=report,
                product=itemObject,
                quantity=post_item.get("quantity"),
                price=post_item.get("price"),
                sale_location=post_item.get("sale_location"),
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
