from .models import Product, ProductionReportDetails, ProductionReport, LLLocation, Garden
from .forms import ProductionReportForm, ProductionProductForm
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
import json

def get_locations(request):
    city = request.GET.get('city')
    locations = LLLocation.objects.filter(living_lab=city).order_by('name')
    #return JsonResponse(list(locations), safe=False)
    return render(request, 'hr/locations_dropdown_list_options.html', {'locations': locations})

def get_gardens(request):
    city = request.GET.get('city')
    location = request.GET.get('location')
    gardens = Garden.objects.filter(location_id=location).order_by('name')
    return render(request, 'hr/gardens_dropdown_list_options.html', {'gardens': gardens})

def get_post_report(request):
    if request.method == "GET":
        report = ProductionReportForm()
        item_form = ProductionProductForm()
        return render(
            request,
            "productionReport_form.html",
            {
                "productionReport_form": report,
                "item_form": item_form,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = ProductionReport.objects.create(
            production_date=data.get("production_date"),
            city=data.get("city"),
            location=LLLocation.objects.get(name=data.get("location")),
            garden=Garden.objects.get(name=data.get("garden")),
            user=request.user,
        )
        for post_item in data.get("items", []):
            itemObject = Product.objects.get(name=post_item.get("item_name"))
            ProductionReportDetails.objects.create(
                report_id=report,
                name=itemObject,
                quantity=post_item.get("quantity"),
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
    
def get_products_by_city(request):
    """
    AJAX view to get products filtered by city
    """
    city_id = request.GET.get('city_id')
    
    if city_id:
        try:
            products = Product.objects.filter(living_lab=city_id).values('name', 'unit', 'cultivation_type')
            product_list = list(products)
        except:
            product_list = []
    else:
        product_list = []
    
    return JsonResponse({'products': product_list})
