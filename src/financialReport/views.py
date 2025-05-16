from .models import FinancialReport
from .forms import FinancialReportForm
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json


def get_post_report(request):
    if request.method == "GET":
        report = FinancialReportForm()
        return render(
            request,
            "financialForm.html",
            {
                "financialForm": report,
            },
        )

    elif request.method == "POST":
        data = json.loads(request.body)
        report = FinancialReport.objects.create(
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            city=data.get("city"),
            location=data.get("location"),
            garden=data.get("garden"),
            user=request.user,
            currency=data.get("currency"),
            exp_workforce=data.get("exp_workforce"),
            exp_purchase=data.get("exp_purchase"),
            exp_others=data.get("exp_others"),
            exp_others_desc=data.get("exp_others_desc"),
            fun_feed4food=data.get("fun_feed4food"),
            fun_others=data.get("fun_others"),
            fun_others_desc=data.get("fun_others_desc"),
            rev_restaurant=data.get("rev_restaurant"),
            rev_others=data.get("rev_others"),
            rev_others_desc=data.get("rev_others_desc"),
            
        )
        return JsonResponse({"redirect_url": reverse("data_portal")})

    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)#

