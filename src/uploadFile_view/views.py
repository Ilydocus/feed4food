from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone

from productionReport.models import ProductionReport, ProductionReportDetails, Product
from inputReport.models import InputReport, InputReportDetails, Input
from plantingRepot.models import PlantingReport, PlantingReportDetails
from .models import StagedRow
from uploadFile.matching import validate_row, split_crop_list


def _resolve_row(row_data: dict, living_lab: str) -> tuple:
    """Runs validate_row and returns (status, message, corrected_data)
    with resolved fields (matched_product/input, resolved_quantity) baked
    in as plain values ready for a JSONField."""
    result = validate_row(row_data, living_lab)
    bucket = result["bucket"]

    status_map = {
        "duplicate": "duplicate",
        "needs_suggestion": "needs_review",
        "error": "needs_review",
        "not_supported": "not_supported",
        "ignored": "ignored",
        "unknown": "unknown",
    }
    status = status_map.get(bucket, "needs_review")
    message = result.get("message", "")

    corrected = dict(row_data)
    corrected.pop("suggestions", None)  # clear any stale suggestions from a previous attempt
    corrected.pop("suggestion_field", None)

    if bucket == "needs_suggestion":
        corrected["suggestions"] = result.get("suggestions", [])
        corrected["suggestion_field"] = result.get("suggestion_field")

    if bucket == "inserted":
        # Dispatch on the explicit report_type key rather than "which keys
        # are present" - matched_product is now shared by both Harvest and
        # Planting rows, so duck-typing on it would collide between the two.
        report_type = result.get("report_type")
        corrected["report_type"] = report_type

        # NOTE: store pk, not name - commit_batch looks these up by pk
        # (Product.objects.filter(pk=...) / Input.objects.filter(pk=...)).
        # Storing .name here silently produced None matches at commit time.
        if "product" in result:
            corrected["matched_product"] = result["product"].pk
        if "input" in result:
            corrected["matched_input"] = result["input"].pk
        if "planting_unit" in result:
            corrected["planting_unit"] = result["planting_unit"]
        corrected["resolved_quantity"] = result.get("quantity")

        if report_type == "input" and not corrected.get("area"):
            status = "needs_review"
            message = "Area is required for this row but wasn't in the Excel - please fill it in."
        else:
            status = "auto_approved"

    return status, message, corrected


@login_required
def uploadFile_list_batch(request, batch_id):
    rows = StagedRow.objects.filter(upload_batch=batch_id).order_by("source_row_number")

    grouped = {}
    for row in rows:
        grouped.setdefault(row.status, []).append(row)

    blocking_count = rows.filter(status__in=StagedRow.BLOCKING_STATUSES).count()
    already_committed = rows.filter(status="committed").exists()

    context = {
        "batch_id": batch_id,
        "grouped": grouped,
        "can_commit": blocking_count == 0 and not already_committed and rows.exists(),
        "blocking_count": blocking_count,
    }
    return render(request, "uploadFile_list.html", context)


@login_required
def uploadFile_details(request, row_id):
    row = get_object_or_404(StagedRow, id=row_id)
    crops = split_crop_list(row.corrected_data.get("crop_raw"))
    can_split = len(crops) > 1

    split_preview = None
    if can_split and request.GET.get("split"):
        editable_keys = [
            k for k in row.corrected_data.keys()
            if k not in (
                "matched_product", "matched_input", "resolved_quantity",
                "suggestions", "suggestion_field", "report_type", "planting_unit",
            )
        ]
        split_preview = []
        for i, crop in enumerate(crops):
            fields = {k: (crop if k == "crop_raw" else row.corrected_data.get(k)) for k in editable_keys}
            split_preview.append({"index": i, "fields": fields})

    return render(request, "uploadFile_details.html", {
        "row": row, "can_split": can_split, "split_preview": split_preview,
    })


@login_required
def confirm_split(request, row_id):
    """User has reviewed/edited the split preview blocks - actually create
    the new StagedRows now and supersede the original row."""
    row = get_object_or_404(StagedRow, id=row_id)

    if request.method != "POST":
        return redirect("uploadFile_details", row_id=row.id)

    crops = split_crop_list(row.corrected_data.get("crop_raw"))
    if len(crops) <= 1:
        messages.warning(request, "Nothing to split.")
        return redirect("uploadFile_details", row_id=row.id)

    editable_keys = [
        k for k in row.corrected_data.keys()
        if k not in (
            "matched_product", "matched_input", "resolved_quantity",
            "suggestions", "suggestion_field", "report_type", "planting_unit",
        )
    ]

    created = 0
    for i in range(len(crops)):
        new_row_data = {
            k: request.POST.get(f"row__{i}__{k}", row.corrected_data.get(k))
            for k in editable_keys
        }
        status, message, corrected = _resolve_row(new_row_data, row.living_lab)

        StagedRow.objects.create(
            upload_batch=row.upload_batch,
            source_row_number=row.source_row_number,
            action_type=row.action_type,
            living_lab=row.living_lab,
            raw_data=row.raw_data,  # keep original combined value for traceability
            corrected_data=corrected,
            message=message,
            status=status,
            uploaded_by=row.uploaded_by,
        )
        created += 1

    row.status = "rejected"
    row.message = f"Split into {created} rows."
    row.reviewed_at = timezone.now()
    row.save()

    messages.success(request, f"Row split into {created} rows and saved.")
    return redirect("uploadFile_list_batch", batch_id=row.upload_batch)


@login_required
def edit_row(request, row_id):
    """User edits a needs_review row - re-run validation instead of blindly
    trusting the edit, since a typo fix might still not match anything."""
    row = get_object_or_404(StagedRow, id=row_id)

    if request.method != "POST":
        return redirect("uploadFile_details", row_id=row.id)

    updated = dict(row.corrected_data)
    for key in updated.keys():
        if key in request.POST:
            updated[key] = request.POST.get(key)

    status, message, corrected = _resolve_row(updated, row.living_lab)

    row.status = status
    row.message = message
    row.corrected_data = corrected
    row.reviewed_at = timezone.now()
    row.save()

    if row.status in ("auto_approved", "approved"):
        messages.success(request, "Row now resolves correctly.")
    else:
        messages.warning(request, row.message)

    # Send the user back to this row's details page (not the batch list) so
    # they can actually see any new "did you mean?" suggestions or the
    # updated error message. Redirecting to the list page here was hiding
    # suggestions from the user entirely.
    return redirect("uploadFile_details", row_id=row.id)


@login_required
def apply_suggestion(request, row_id):
    """User clicked a 'did you mean X?' suggestion - apply it to the
    relevant field and re-validate, same as a manual edit would."""
    row = get_object_or_404(StagedRow, id=row_id)
    if request.method != "POST":
        return redirect("uploadFile_details", row_id=row.id)

    field = request.POST.get("field")  # "crop_raw" or "input_name_raw"
    value = request.POST.get("value")
    if field not in ("crop_raw", "input_name_raw") or not value:
        messages.error(request, "Invalid suggestion.")
        return redirect("uploadFile_details", row_id=row.id)

    updated = dict(row.corrected_data)
    updated[field] = value

    status, message, corrected = _resolve_row(updated, row.living_lab)

    row.status = status
    row.message = message
    row.corrected_data = corrected
    row.reviewed_at = timezone.now()
    row.save()

    if row.status in ("auto_approved", "approved"):
        messages.success(request, "Row now resolves correctly.")
    else:
        messages.warning(request, row.message)

    # Same fix as edit_row - stay on the row's details page after applying
    # a suggestion, rather than bouncing back to the batch list.
    return redirect("uploadFile_details", row_id=row.id)


@login_required
def reject_row(request, row_id):
    row = get_object_or_404(StagedRow, id=row_id)
    if request.method == "POST":
        row.status = "rejected"
        row.reviewed_at = timezone.now()
        row.save()
        messages.warning(request, "Row rejected.")
    return redirect("uploadFile_list_batch", batch_id=row.upload_batch)


@login_required
def commit_batch(request, batch_id):
    if request.method != "POST":
        return redirect("uploadFile_list_batch", batch_id=batch_id)

    rows = StagedRow.objects.filter(upload_batch=batch_id)

    blocking = rows.filter(status__in=StagedRow.BLOCKING_STATUSES)
    if blocking.exists():
        messages.error(request, f"{blocking.count()} row(s) still need review before this batch can be entered.")
        return redirect("uploadFile_list_batch", batch_id=batch_id)

    insertable = rows.filter(status__in=StagedRow.INSERTABLE_STATUSES)

    with transaction.atomic():
        for row in insertable:
            data = row.corrected_data
            living_lab = row.living_lab
            report_type = data.get("report_type")

            if report_type == "input":
                # Spraying / Root Irrigation / Insect release -> InputReport
                report, _ = InputReport.objects.get_or_create(
                    application_date=data.get("production_date"),
                    city=living_lab,
                    user=row.uploaded_by,
                )
                InputReportDetails.objects.create(
                    report_id=report,
                    name_input=Input.objects.filter(pk=data["matched_input"]).first(),
                    name_product=Product.objects.filter(pk=data.get("matched_product")).first(),
                    area=float(data.get("area")),
                    quantity=float(data.get("resolved_quantity")),
                )
            elif report_type == "harvest":
                report, _ = ProductionReport.objects.get_or_create(
                    production_date=data.get("production_date"),
                    city=living_lab,
                    user=row.uploaded_by,
                )
                ProductionReportDetails.objects.create(
                    report_id=report,
                    name=Product.objects.filter(pk=data["matched_product"]).first(),
                    quantity=float(data.get("resolved_quantity")),
                )
            elif report_type == "planting":
                report, _ = PlantingReport.objects.get_or_create(
                    planting_date=data.get("production_date"),
                    city=living_lab,
                    user=row.uploaded_by,
                )
                PlantingReportDetails.objects.create(
                    report_id=report,
                    name=Product.objects.filter(pk=data["matched_product"]).first(),
                    area_quantity_planted=float(data.get("resolved_quantity")),
                    planting_unit=data.get("planting_unit"),
                )

            row.status = "committed"
            row.save()

    messages.success(request, f"{insertable.count()} row(s) entered into the database.")
    return redirect("upload_file")