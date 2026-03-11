from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Technology
from portfolio.models import Profile

def get_profile():
    return Profile.objects.filter(is_active=True).first()

@login_required
def project_list(request):
    profile = get_profile()
    projects = Project.objects.prefetch_related('technologies').all()
    technologies = Technology.objects.all()
    featured = projects.filter(is_featured=True)
    context = {
        'profile': profile,
        'projects': projects,
        'featured': featured,
        'technologies': technologies,
    }
    return render(request, 'projects/project_list.html', context)


@login_required
def project_detail(request, slug):
    profile = get_profile()
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.filter(
        technologies__in=project.technologies.all()
    ).exclude(id=project.id).distinct()[:3]
    context = {'profile': profile,'project': project, 'related': related}
    return render(request, 'projects/project_detail.html', context)

