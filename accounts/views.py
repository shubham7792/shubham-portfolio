from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django import forms
from portfolio.models import Profile

def get_profile():
    return Profile.objects.filter(is_active = True).first()


class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


def register_view(request):
    profile = get_profile()
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = CustomRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form,'profile': profile})


def login_view(request):
    profile = get_profile()
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', '/')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(next_url)
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url,'profile': profile})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


def get_jwt_token(request):
    """API endpoint to get JWT tokens for authenticated session user"""
    if not request.user.is_authenticated:
        from django.http import JsonResponse
        return JsonResponse({'error': 'Authentication required'}, status=401)

    refresh = RefreshToken.for_user(request.user)
    from django.http import JsonResponse
    return JsonResponse({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })
