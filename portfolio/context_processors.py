from .models import Profile

def profile_context(request):
    profile = Profile.objects.filter(is_active=True).first()
    return {'profile': profile}
