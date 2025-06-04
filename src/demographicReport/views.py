from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import UnderrepresentedGroups, DemographicReport, DemographicReportPerUnderrepresentedGroups
from .forms import DemographicGroupForm, DemographicReportForm
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json


@require_GET
def get_groups_by_city(request):
    city = request.GET.get('city')
    
    if not city:
        return JsonResponse({'groups': []})
    
    # Get the groups registered to this city
    groups = UnderrepresentedGroups.objects.filter(
        living_lab=city  
    ).values('id', 'name')
    
    return JsonResponse({
        'groups': list(groups)
    })

def get_post_report(request):
    if request.method == "GET":
        report = DemographicReportForm()
        group_form = DemographicGroupForm()
        return render(
            request,
            "demographicForm.html",
            {
                "demographicForm": report,
                "demographicGroup_form": group_form,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = DemographicReport.objects.create(
            data_date=data.get("data_date"),
            city=data.get("city"),
            total_population=data.get("total_population"),
            user=request.user,
        )
        for post_item in data.get("groups", []):
            groupObject = UnderrepresentedGroups.objects.get(name=post_item.get("group_name"))
            DemographicReportPerUnderrepresentedGroups.objects.create(
                report_id=report,
                name=groupObject,
                population=post_item.get("population"),
            )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
