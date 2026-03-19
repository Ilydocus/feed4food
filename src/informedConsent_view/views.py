from django.shortcuts import render
from django.http import FileResponse, Http404
import os
from django.conf import settings

# def informedConsent_show(request):
#     context = {
#         'title': 'Informed consent',
#         'description': 'View again the informed consent information.',
#     }
#     return render(request, 'informedConsent_view/templates/informedConsent_show.html', context)

def download_informedConsent(request):
    # Location of the file
    file_path = os.path.join(settings.BASE_DIR, 'static/files/Informed_consent_Feed4Food.pdf')
    
    try:
        # Open the file and return as response
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="Informed_consent_Feed4Food.pdf"'
        return response
    except FileNotFoundError:
        raise Http404("File not found")
