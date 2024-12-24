from .models import Items, ProduceReportDetails, ProduceReport
from .forms import ProduceReportForm, ProduceItemForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json

def get_item_attributes(request, name):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    
    item_obj = get_object_or_404(Items, name=name)
    return JsonResponse(model_to_dict(item_obj))

def get_post_report(request):
    if request.method == 'GET':
        report = ProduceReportForm()
        item_form = ProduceItemForm()
        return render(request, 'report_form.html', {
            'report_form': report,
            'item_form': item_form,
        })

    elif request.method == 'POST':
        data = json.loads(request.body)
        report = ProduceReport.objects.create(
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            city=data.get('city'),
            location=data.get('location'),
            garden=data.get('garden'),
            user=request.user,
        )
        for post_item in data.get('items', []):
            itemObject = Items.objects.get(name=post_item.get('item_name'))
            ProduceReportDetails.objects.create(
                report=report,
                item=itemObject,
                quantity=post_item.get('quantity'),
            )
        return JsonResponse({'status': 'success'})

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)