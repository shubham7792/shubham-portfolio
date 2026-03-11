from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from .models import Profile, Skill, Education, Experience
import os


def get_profile():
    return Profile.objects.filter(is_active=True).first()


def home(request):
    profile = get_profile()
    context = {'profile': profile}
    return render(request, 'portfolio/home.html', context)


@login_required
def about(request):
    profile = get_profile()
    skills = Skill.objects.all()
    education = Education.objects.all()
    experience = Experience.objects.all()

    skills_by_category = {}
    for skill in skills:
        cat = skill.get_category_display()
        if cat not in skills_by_category:
            skills_by_category[cat] = []
        skills_by_category[cat].append(skill)

    context = {
        'profile': profile,
        'skills': skills,
        'skills_by_category': skills_by_category,
        'education': education,
        'experience': experience,
    }
    return render(request, 'portfolio/about.html', context)


def download_cv(request):
    profile = get_profile()
    if not profile or not profile.cv_file:
        raise Http404("CV not found")
    file_path = profile.cv_file.path
    if not os.path.exists(file_path):
        raise Http404("CV file not found")
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="CV_{profile.name.replace(" ", "_")}.pdf"'
    return response

skills = ["HTML","CSS","JavaScript","Python","Django","Git","Bootstrap","PostgreSQL"]

context = {
    "skills": skills
}