from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import FeedbackForm

def feedback_view(request):
    # Get the previous page to redirect back to after submission
    referer = request.META.get('HTTP_REFERER', '/')
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback!')
            # Redirect back to the referring page
            return redirect('home')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback_form.html', {
        'form': form,
        'referer': referer
    })