from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import uuid
import pandas as pd

from productionReport.models import Garden
from uploadFile_view.models import StagedRow
from .parser import parse_file
from .matching import validate_row

# Buckets returned by validate_row() -> StagedRow status
BUCKET_TO_STATUS = {
    "inserted": "auto_approved",
    "duplicate": "duplicate",
    "error": "needs_review",       # user can try to fix in the review UI
    "not_supported": "not_supported",
    "ignored": "ignored",
    "unknown": "unknown",
}


def _json_safe(row_data: dict) -> dict:
    safe = {}
    for key, value in row_data.items():
        if hasattr(value, "isoformat"): 
            safe[key] = value.isoformat()
        elif isinstance(value, float) and pd.isna(value):  
            safe[key] = None
        else:
            safe[key] = value
    return safe


@login_required
def upload_file_view(request):
    if request.method == "GET":
        gardens = Garden.objects.all().order_by("name")
        return render(request, "upload_file_form.html", {"gardens": gardens})

    elif request.method == "POST":
        uploaded_file = request.FILES.get("file")
        template_id = request.POST.get("template")
        garden_id = request.POST.get("garden")

        if not uploaded_file:
            messages.error(request, "No file selected.")
            return redirect("upload_file")

        if not garden_id:
            messages.error(request, "Please select a garden.")
            return redirect("upload_file")

        garden = Garden.objects.filter(pk=garden_id).first()
        if garden is None:
            messages.error(request, "Selected garden not found.")
            return redirect("upload_file")

        living_lab = garden.living_lab

        try:
            parsed_rows = parse_file(uploaded_file, template_id)
        except Exception as e:
            messages.error(request, f"Could not read or parse file: {e}")
            return redirect("upload_file")

        upload_batch_id = str(uuid.uuid4())

        for row_data in parsed_rows:
            result = validate_row(row_data, living_lab, garden)
            bucket = result["bucket"]
            status = BUCKET_TO_STATUS.get(bucket, "needs_review")

            corrected = _json_safe(row_data)

            if bucket == "inserted":
                if "product" in result:
                    corrected["matched_product"] = result["product"].name
                if "input" in result:
                    corrected["matched_input"] = result["input"].name
                corrected["resolved_quantity"] = result.get("quantity")

                if "input" in result:
                    corrected["area"] = None
                    status = "needs_review"
                    result["message"] = (
                        "Area is required for this row but wasn't in the Excel - please fill it in."
                    )

            StagedRow.objects.create(
                upload_batch=upload_batch_id,
                source_row_number=row_data.get("source_row_number"),
                action_type=row_data.get("action_type_raw") or "unknown",
                garden=garden,
                raw_data=_json_safe(row_data),
                corrected_data=corrected,
                message=result.get("message", ""),
                status=status,
                uploaded_by=request.user,
            )

        messages.success(request, "File uploaded and parsed.")
        return redirect("uploadFile_list_batch", batch_id=upload_batch_id)

    else:
        messages.error(request, "Only GET/POST allowed.")
        return redirect("upload_file")