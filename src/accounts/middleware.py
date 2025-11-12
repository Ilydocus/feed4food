from django.shortcuts import redirect
from django.urls import reverse
from .models import EthicsConsent


class InactiveUserRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_active:
            return redirect("pending_activation")  # Redirect inactive users
        return self.get_response(request)
    
class EthicsConsentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that don't require ethics consent should be listed here
        self.exempt_urls = [
            reverse('ethics_consent'),
            reverse('logout'),
            #'/admin/',
            #'/static/',
            #'/media/',
        ]
    
    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if current path is exempted
            path = request.path
            is_exempt = any(path.startswith(url) for url in self.exempt_urls)
            
            if not is_exempt:
                # Check if user has given ethics consent
                consent, created =EthicsConsent.objects.get_or_create(user=request.user)
                
                if not consent.has_given_consent:
                    return redirect('ethics_consent')
        
        response = self.get_response(request)
        return response
    

