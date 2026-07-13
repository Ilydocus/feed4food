from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd
import uuid
from uploadFile_view.models import StagedRow 
from .parser import parse_file
from .matching import validate_row

@login_required
def upload_file_view(request):
    if request.method == "GET":
        return render(request, "upload_file_form.html")

    elif request.method == "POST":
        uploaded_file = request.FILES.get("file")
        template_id = request.POST.get("template")

        if not uploaded_file:
            messages.error(request, "No file selected.")
            return redirect("upload_file")

        # 1. Route by `template` value to correct parser
        try:
            parsed_rows = parse_file(uploaded_file, template_id)
        except Exception as e:
            messages.error(request, f"Could not read or parse file: {e}")
            return redirect("upload_file")

        living_lab = getattr(request.user, 'living_lab', "Default Lab") 
        upload_batch_id = str(uuid.uuid4()) 

        for row_data in parsed_rows:
            validation_result = validate_row(row_data, living_lab) 
            
            status = "needs_review"
            if validation_result['bucket'] == "error":
                status = "rejected"
            elif validation_result['bucket'] == "inserted":
                status = "auto_approved"

            StagedRow.objects.create(
                upload_batch=upload_batch_id,
                source_row_number=row_data.get("source_row_number"),
                action_type=row_data.get("action_type_raw", "unknown"),
                raw_data=row_data,
                corrected_data=row_data, 
                status=status,
                uploaded_by=request.user
            )

        messages.success(request, "File uploaded and parsed.")
        return redirect("uploadFile_list") 

    else:
        messages.error(request, "Only GET/POST allowed.")
        return redirect("upload_file")