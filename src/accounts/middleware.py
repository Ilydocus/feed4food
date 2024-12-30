from django.shortcuts import redirect

class InactiveUserRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_active:
            return redirect('pending_activation')  # Redirect inactive users
        return self.get_response(request)
