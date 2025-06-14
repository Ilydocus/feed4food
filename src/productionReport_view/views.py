from django.shortcuts import render, get_object_or_404
from productionReport.models import ProductionReport, ProductionReportDetails, Product, LLLocation, Garden
from productionReport.forms import ProductionProductForm, ProductionReportForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def productionReport_list(request):
    reports = ProductionReport.objects.filter(user=request.user)
    return render(request, "productionReport_list.html", {"reports": reports})


def productionReport_details(request, report_id):
    report = ProductionReport.objects.get(report_id=report_id)
    items = Product.objects.all()
    return render(request, "productionReport_details.html", {"report": report, "items": items})


def edit_report(request, report_id):
    report = get_object_or_404(ProductionReport, report_id=report_id)
    old_report_items = ProductionReportDetails.objects.filter(report_id=report_id)

    if request.method == "POST":
        data = json.loads(request.body)
        old_report_items.delete()
        for post_item in data.get("items", []):
            itemObject = Product.objects.get(name=post_item.get("item_name"))
            ProductionReportDetails.objects.create(
                report_id=report,
                name=itemObject,
                quantity=post_item.get("quantity"),
            )

        report.production_date = data.get("production_date")
        report.city = data.get("city")
        report.location = LLLocation.objects.get(name=data.get("location"))
        report.garden = Garden.objects.get(name=data.get("garden"))
        report.save()
        return JsonResponse({"redirect_url": reverse("productionReport_list")})

    if request.method == "GET":
        item_form_template = ProductionProductForm()
        report_form = ProductionReportForm(instance=report)
        initial_data = []
        for item in old_report_items:
            initial_data.append({
                'name': item.name,
                'quantity': item.quantity,
            })
        formset = formset_factory(ProductionProductForm, extra=0)(
            initial=initial_data
        )
        return render(
            request,
            "productionReport_edit.html",
            {
                "item_form": item_form_template,
                "productionReport_form": report_form,
                "old_report_items": old_report_items,
                "formset": formset,
            },
        )
