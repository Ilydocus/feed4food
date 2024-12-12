from .models import ProduceItem, ProduceReport, ItemName
from .forms import DateRangeForm
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.safestring import mark_safe
import json

class ProduceReportView(View):

    def get(self, request):
        date_form = DateRangeForm()
        item_names = ItemName.objects.values_list('name', flat=True)
        return render(request, 'report_form.html', {
            'date_form': date_form,
            'item_names': mark_safe(json.dumps(list(item_names)))
        })
    
    def post(self, request):
        data = json.loads(request.body)
        report = ProduceReport.objects.create(
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            user=request.user
        )
        
        for item in data.get('items', []):
            ProduceItem.objects.create(
                report=report,
                item_name=item.get('item_name'),
                location=item.get('location'),
                item_type=item.get('type'),
                quantity=item.get('quantity'),
            )

        return JsonResponse({'status': 'success'})