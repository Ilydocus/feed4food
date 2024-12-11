from django.shortcuts import render, redirect
from .models import ProduceReport
from .forms import ProduceReportForm
from django.contrib.auth.decorators import login_required


# def index(request):
#     reports = ProduceReport.objects.all()
#     return render(request, 'index.html', {'reports': reports})

@login_required
def daily_report_form(request):
    if request.method == 'POST':
        form = ProduceReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daily_report_form')
    else:
        form = ProduceReportForm()

    reports = ProduceReport.objects.all()
    return render(request, 'index.html', {'form': form, 'reports': reports})


from django.http import JsonResponse
from .forms import DateRangeForm, ItemSelectionForm, ItemDetailForm
from .models import Item, ItemDetail

def report_form(request):
    if request.method == 'POST':
        date_form = DateRangeForm(request.POST)
        item_form = ItemSelectionForm(request.POST)
        detail_form = ItemDetailForm(request.POST)
        
        if date_form.is_valid() and item_form.is_valid() and detail_form.is_valid():
            # Process and save data
            item = item_form.cleaned_data['item']
            breed = detail_form.cleaned_data.get('breed', None)
            quantity = detail_form.cleaned_data.get('quantity', 0)
            
            ItemDetail.objects.create(item=item, key="Breed", value=breed, quantity=quantity)
            #return redirect('success_page')
    else:
        date_form = DateRangeForm()
        item_form = ItemSelectionForm()
        detail_form = ItemDetailForm()

    return render(request, 'report_form.html', {
        'date_form': date_form,
        'item_form': item_form,
        'detail_form': detail_form,
    })

def item_details(request, item_id):
    # Return details based on the selected item
    item = Item.objects.get(id=item_id)
    if item.requires_details:
        response = {
            "fields": [
                {"name": "breed", "label": "Breed", "type": "text"},
                {"name": "quantity", "label": "Quantity", "type": "number"}
            ]
        }
    else:
        response = {"fields": []}
    return JsonResponse(response)


# @login_required
# def daily_report_form(request):
#     return render(request, 'report_form.html')
