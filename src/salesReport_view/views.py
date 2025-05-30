from django.shortcuts import render, get_object_or_404
from report.models import Product
from salesReport.models import SalesReport, SalesReportDetails
from salesReport.forms import SalesReportForm, SalesActionForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def salesReport_list(request):
    reports = SalesReport.objects.filter(user=request.user)
    return render(request, "salesReport_list.html", {"reports": reports})


def salesReport_details(request, report_id):
    report = SalesReport.objects.get(report_id=report_id)
    items = Product.objects.all()
    return render(request, "salesReport_details.html", {"report": report, "items": items})


def edit_report(request, report_id):
    report = get_object_or_404(SalesReport, report_id=report_id)
    old_report_items = SalesReportDetails.objects.filter(report_id=report_id)

    if request.method == "POST":
        data = json.loads(request.body)
        old_report_items.delete()
        for post_item in data.get("items", []):
            itemObject = Product.objects.get(name=post_item.get("item_name"))
            SalesReportDetails.objects.create(
                report_id=report,
                product=itemObject,
                quantity=post_item.get("quantity"),
                sale_date=post_item.get("sale_date"),
                sale_location=post_item.get("sale_location"),
                price=post_item.get("price"),
            )

        report.city = data.get("city")
        report.location = data.get("location")
        report.garden = data.get("garden")
        report.currency = data.get("currency")
        report.save()
        return JsonResponse({"redirect_url": reverse("salesReport_list")})

    if request.method == "GET":
        item_form_template = SalesActionForm()
        report_form = SalesReportForm(instance=report)
        formset = formset_factory(SalesActionForm, extra=0)(
            initial=old_report_items.values()
        )
        return render(
            request,
            "salesReport_edit.html",
            {
                "salesList_form": item_form_template,
                "sales_form": report_form,
                "old_report_items": old_report_items,
                "formset": formset,
            },
        )

