from .models import ProfessionalProfile

class UserContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        user_context = {}
        if request.user.is_authenticated:
            try:
                profile = ProfessionalProfile.objects.get(user=request.user)
                user_context['user_profile'] = profile
            except ProfessionalProfile.DoesNotExist:
                pass
        request.user_context = user_context
        response = self.get_response(request)
        return response