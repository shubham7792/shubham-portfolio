from contact.models import Message


def dashboard_context(request):
    """Inject new message count into all dashboard templates."""
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        new_count = Message.objects.filter(status='new').count()
    else:
        new_count = 0
    return {'new_messages_count': new_count}