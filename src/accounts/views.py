from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect('pending_activation')  # Redirect here after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def pending_activation(request):
    return render(request, 'pending_activation.html')
