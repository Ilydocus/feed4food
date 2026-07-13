from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd


@login_required
def upload_file_view(request):
    if request.method == "GET":
        return render(request, "upload_file_form.html")

    elif request.method == "POST":
        uploaded_file = request.FILES.get("file")
        template = request.POST.get("template")

        if not uploaded_file:
            messages.error(request, "No file selected.")
            return redirect("upload_file")

        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file, header=None)
            else:
                df = pd.read_excel(uploaded_file, header=None)
        except Exception as e:
            messages.error(request, f"Could not read file: {e}")
            return redirect("upload_file")

        # TODO: route by `template` value to correct parser
        # TODO: parse df -> staged rows -> save to staging model
        # TODO: redirect to uploadFile_view review list

        messages.success(request, "File uploaded and parsed.")
        return redirect("uploadFile_list")

    else:
        messages.error(request, "Only GET/POST allowed.")
        return redirect("upload_file")