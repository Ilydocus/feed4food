from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import StagedRow


def uploadFile_list(request):
    rows = StagedRow.objects.filter(status="needs_review").order_by("upload_batch", "source_row_number")
    return render(request, "uploadFile_list.html", {"rows": rows})


def uploadFile_details(request, row_id):
    row = get_object_or_404(StagedRow, id=row_id)
    return render(request, "uploadFile_details.html", {"row": row})


def approve_row(request, row_id):
    row = get_object_or_404(StagedRow, id=row_id)

    if request.method == "POST":
        # overwrite corrected_data with user-edited values from the form
        updated_data = {}
        for key in row.corrected_data.keys():
            updated_data[key] = request.POST.get(key, row.corrected_data[key])
        row.corrected_data = updated_data

        # TODO: write row.corrected_data into real report tables here

        row.status = "approved"
        row.reviewed_at = timezone.now()
        row.save()
        messages.success(request, "Row approved and saved.")

    return redirect("uploadFile_list")


def reject_row(request, row_id):
    row = get_object_or_404(StagedRow, id=row_id)
    row.status = "rejected"
    row.reviewed_at = timezone.now()
    row.save()
    messages.info(request, "Row rejected.")
    return redirect("uploadFile_list")