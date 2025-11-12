from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import EthicsConsent


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect("pending_activation")  # Redirect here after registration
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def pending_activation(request):
    return render(request, "pending_activation.html")

@login_required
def ethics_consent(request):
    consent, created = EthicsConsent.objects.get_or_create(user=request.user)
    
    # If consent already given, redirect to home
    if consent.has_given_consent:
        return redirect('home')
    
    if request.method == 'POST':
        if request.POST.get('accept') == 'yes':
            consent.has_given_consent = True
            consent.consent_given_at = timezone.now()
            consent.save()
            
            # Redirect to the page they were trying to access, or home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            # User did not give consent - they are logged out
            return redirect('logout')
    
    return render(request, 'ethics_consent.html')


