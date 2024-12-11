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

# @login_required
# def daily_report_form(request):
#     return render(request, 'report_form.html')
