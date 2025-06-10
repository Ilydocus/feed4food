from .models import InputReportDetails, InputReport, Input
from productionReport.models import Product, LLLocation, Garden
from .forms import InputReportForm, InputListForm
from django.shortcuts import render

from django.urls import reverse
from django.http import JsonResponse
import json

def get_post_report(request):
    if request.method == "GET":
        report = InputReportForm()
        item_form = InputListForm()
        return render(
            request,
            "inputReport.html",
            {
                "inputForm": report,
                "inputsApplied_form": item_form,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = InputReport.objects.create(
            application_date=data.get("application_date"),
            city=data.get("city"),
            location=LLLocation.objects.get(name=data.get("location")),
            garden=Garden.objects.get(name=data.get("garden")),
            user=request.user,
        )
        for post_item in data.get("inputs", []):
            productObject = Product.objects.get(name=post_item.get("name_product"))
            inputObject = Input.objects.get(name=post_item.get("name_input"))
            InputReportDetails.objects.create(
                report_id=report,
                name_product=productObject,
                name_input=inputObject,
                area=post_item.get("area"),
                quantity=post_item.get("quantity"),
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
    
def get_inputs_by_city(request):
    """
    AJAX view to get inputs filtered by city
    """
    city_id = request.GET.get('city_id')
    
    if city_id:
        try:
            inputs = Input.objects.filter(living_lab=city_id).values('name', 'unit')
            input_list = list(inputs)
        except:
            input_list = []
    else:
        input_list = []
    
    return JsonResponse({'inputs': input_list})

