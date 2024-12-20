from .models import Items, ProduceReport,ProduceReportDetails
from .forms import DateRangeForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.forms.models import model_to_dict
# from django.contrib.gis.geos import Point
from django.conf import settings
import json

def get_item_attributes(request, name):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    
    item_obj = get_object_or_404(Items, name=name)
    return JsonResponse(model_to_dict(item_obj))

def get_post_report(request):
    if request.method == 'GET':
        date_form = DateRangeForm()
        item_names = Items.objects.values_list('name', flat=True)
        return render(request, 'report_form.html', {
            'date_form': date_form,
            'item_names': mark_safe(json.dumps(list(item_names))),
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
        })

    elif request.method == 'POST':
        data = json.loads(request.body)
        # location = Point(*data.get('location'))
        location = 'potato'
        report = ProduceReport.objects.create(
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            user=request.user,
            location=location
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
    