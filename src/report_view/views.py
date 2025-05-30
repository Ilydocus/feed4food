from django.shortcuts import render, get_object_or_404
from productionReport.models import ProductionReport, ProductionReportDetails, Product
from productionReport.forms import ProduceItemForm, ProductionReportForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def report_list(request):
    reports = ProductionReport.objects.filter(user=request.user)
    return render(request, "report_list.html", {"reports": reports})


def report_details(request, report_id):
    report = ProductionReport.objects.get(report_id=report_id)
    items = Product.objects.all()
    return render(request, "report_details.html", {"report": report, "items": items})


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

        report.start_date = data.get("start_date")
        report.end_date = data.get("end_date")
        report.city = data.get("city")
        report.location = data.get("location")
        report.garden = data.get("garden")
        report.save()
        return JsonResponse({"redirect_url": reverse("report_list")})

    if request.method == "GET":
        item_form_template = ProduceItemForm()
        report_form = ProductionReportForm(instance=report)
        formset = formset_factory(ProduceItemForm, extra=0)(
            initial=old_report_items.values()
        )
        return render(
            request,
            "report_edit.html",
            {
                "item_form": item_form_template,
                "report_form": report_form,
                "old_report_items": old_report_items,
                "formset": formset,
            },
        )
