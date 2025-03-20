from django.shortcuts import render
from . import personalDashboard


def dash_page(request):
    return render(request, "personalDashboard.html")

