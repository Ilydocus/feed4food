from django.shortcuts import render, get_object_or_404
from daily_reports.models import ProduceReport, ProduceReportDetails, Items
from daily_reports.forms import ProduceItemForm, ProduceReportForm
from django.forms import formset_factory
from django.http import JsonResponse
import json


def report_list(request):
    reports = ProduceReport.objects.filter(user=request.user)  # Adjust the filter if needed
    return render(request, 'report_list.html', {'reports': reports})

def report_details(request, report_id):
    report = ProduceReport.objects.get(id=report_id)
    return render(request, 'report_details.html', {'report': report})


def edit_report(request, report_id):
    report = get_object_or_404(ProduceReport, id=report_id)
    old_report_items = ProduceReportDetails.objects.filter(report_id=report_id)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        old_report_items.delete()
        for post_item in data.get('items', []):
            itemObject = Items.objects.get(name=post_item.get('item_name'))
            ProduceReportDetails.objects.create(
                report=report,
                item=itemObject,
                quantity=post_item.get('quantity'),
            )

        report.start_date=data.get('start_date')
        report.end_date=data.get('end_date')
        report.city=data.get('city')
        report.location=data.get('location')
        report.garden=data.get('garden')
        report.save()
        return JsonResponse({'status': 'success'})
        
    if request.method == 'GET':
        item_form_template = ProduceItemForm()
        report_form = ProduceReportForm(instance=report)
        formset = formset_factory(ProduceItemForm, extra=0)(initial=old_report_items.values())
        return render(request, 'report_edit.html', {'item_form': item_form_template, 'report_form': report_form, 'old_report_items': old_report_items, 'formset' : formset})