from django.shortcuts import render, get_object_or_404
from financialReport.models import FinancialReport
from financialReport.forms import FinancialReportForm
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse
import json


def financialReport_list(request):
    reports = FinancialReport.objects.filter(user=request.user)
    return render(request, "financialReport_list.html", {"reports": reports})


def financialReport_details(request, report_id):
    report = FinancialReport.objects.get(report_id=report_id)
    return render(request, "financialReport_details.html", {"report": report})


def edit_report(request, report_id):
    report = get_object_or_404(SalesReport, report_id=report_id)
    old_report_items = FinancialReportDetails.objects.filter(report_id=report_id)

    if request.method == "POST":
        data = json.loads(request.body)
        old_report_items.delete()
        
        report.start_date = data.get("start_date")
        report.end_date = data.get("end_date")
        report.city = data.get("city")
        report.location = data.get("location")
        report.garden = data.get("garden")
        report.currency = data.get("currency")
        report.exp_workforce = data.get("exp_workforce")
        report.exp_purchase = data.get("exp_purchase")
        report.exp_others = data.get("exp_others")
        report.exp_others_desc = data.get("exp_others_desc")
        report.fun_feed4food = data.get("fun_feed4food")
        report.fun_others = data.get("fun_others")
        report.fun_others_desc = data.get("fun_others_desc")
        report.rev_restaurant = data.get("rev_restaurant")
        report.rev_others = data.get("rev_others")
        report.rev_others_desc = data.get("rev_others_desc")
        report.save()
        return JsonResponse({"redirect_url": reverse("financialReport_list")})

    if request.method == "GET":
        report_form = FinancialReportForm(instance=report)
        # formset = formset_factory(SalesActionForm, extra=0)(
        #     initial=old_report_items.values()
        # )
        return render(
            request,
            "financialReport_edit.html",
            {
                "financial_form": report_form,
                "old_report_items": old_report_items, #TODO maybe can be removed
                "formset": formset, #TODO maybe can be removed
            },
        )


