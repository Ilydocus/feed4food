from django.shortcuts import render
from . import dashboard


def dash_page(request):
    return render(request, "dashboard.html")
