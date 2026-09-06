from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import uuid
import pandas as pd

from core.reportUtils import PartnerCities
from uploadFile_view.models import StagedRow
from .parser import parse_file
from .matching import validate_row

# Buckets returned by validate_row() -> StagedRow status
BUCKET_TO_STATUS = {
    "inserted": "auto_approved",
    "duplicate": "duplicate",
    "needs_suggestion": "needs_review",  # "did you mean...?" - still needs a human
    "error": "needs_review",             # user can try to fix in the review UI
    "not_supported": "not_supported",
    "ignored": "ignored",
    "unknown": "unknown",
}


def _json_safe(row_data: dict) -> dict:
    """row_data may contain a real date object (production_date) and/or
    pandas NaN for empty Excel cells - neither is valid JSON as-is."""
    safe = {}
    for key, value in row_data.items():
        if hasattr(value, "isoformat"):  # date / datetime
            safe[key] = value.isoformat()
        elif isinstance(value, float) and pd.isna(value):  # pandas NaN
            safe[key] = None
        else:
            safe[key] = value
    return safe


@login_required
def upload_file_view(request):
    if request.method == "GET":
        return render(request, "upload_file_form.html", {"living_labs": PartnerCities.choices})

    elif request.method == "POST":
        uploaded_file = request.FILES.get("file")
        template_id = request.POST.get("template")
        living_lab = request.POST.get("living_lab")

        if not uploaded_file:
            messages.error(request, "No file selected.")
            return redirect("upload_file")

        if not living_lab:
            messages.error(request, "Please select a Living Lab.")
            return redirect("upload_file")

        try:
            parsed_rows = parse_file(uploaded_file, template_id)
        except Exception as e:
            messages.error(request, f"Could not read or parse file: {e}")
            return redirect("upload_file")

        upload_batch_id = str(uuid.uuid4())

        for row_data in parsed_rows:
            result = validate_row(row_data, living_lab)
            bucket = result["bucket"]
            status = BUCKET_TO_STATUS.get(bucket, "needs_review")

            corrected = _json_safe(row_data)

            if bucket == "inserted":
                # Store resolved values as plain strings/numbers, not model
                # instances - JSONField can't hold a Product/Input object.
                if "product" in result:
                    corrected["matched_product"] = result["product"].name
                if "input" in result:
                    corrected["matched_input"] = result["input"].name
                corrected["resolved_quantity"] = result.get("quantity")

                # Spraying/Root Irrigation rows have no `area` column in the
                # Excel at all - always require a human to fill it in, even
                # if the product/input names matched cleanly.
                if "input" in result:
                    corrected["area"] = None
                    status = "needs_review"
                    result["message"] = (
                        "Area is required for this row but wasn't in the Excel - please fill it in."
                    )
            elif bucket == "needs_suggestion":
                corrected["suggestions"] = result.get("suggestions", [])
                corrected["suggestion_field"] = result.get("suggestion_field")

            StagedRow.objects.create(
                upload_batch=upload_batch_id,
                source_row_number=row_data.get("source_row_number"),
                action_type=row_data.get("action_type_raw") or "unknown",
                living_lab=living_lab,
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