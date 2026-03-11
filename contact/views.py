from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .forms import ContactForm
from portfolio.models import Profile


def get_profile():
    return Profile.objects.filter(is_active=True).first()

@login_required
def contact(request):
    profile = get_profile()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
            msg.save()

            # Optional email notification
            try:
                send_mail(
                    subject=f"Portfolio Contact: {msg.subject}",
                    message=f"From: {msg.name} ({msg.email})\n\n{msg.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, "Your message has been sent! I'll get back to you soon.")
            return redirect('contact')
    else:
        form = ContactForm()
        if request.user.is_authenticated:
            form.initial = {
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
            }

    return render(request, 'contact/contact.html', {'form': form, 'profile': profile})
