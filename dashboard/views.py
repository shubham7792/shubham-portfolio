from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils.text import slugify
from django.db.models import Count
from django import forms

from portfolio.models import Profile, Skill, Education, Experience
from projects.models import Project, Technology
from contact.models import Message
from django.contrib.auth.models import User


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

admin_required = user_passes_test(is_admin, login_url='/accounts/login/')


# ── Forms ─────────────────────────────────────────────────────────

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'title', 'tagline', 'bio', 'profile_image',
                  'cv_file', 'github_url', 'linkedin_url', 'twitter_url',
                  'instagram_url', 'email']
        widgets = {
            'name':       forms.TextInput(attrs={'class': 'form-input'}),
            'title':      forms.TextInput(attrs={'class': 'form-input'}),
            'tagline':    forms.TextInput(attrs={'class': 'form-input'}),
            'bio':        forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5}),
            'github_url': forms.URLInput(attrs={'class': 'form-input'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-input'}),
            'twitter_url':  forms.URLInput(attrs={'class': 'form-input'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-input'}),
            'email':      forms.EmailInput(attrs={'class': 'form-input'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'icon_class', 'category', 'proficiency', 'order']
        widgets = {
            'name':       forms.TextInput(attrs={'class': 'form-input'}),
            'icon_class': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'fab fa-python'}),
            'category':   forms.Select(attrs={'class': 'form-input'}),
            'proficiency': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 100}),
            'order':      forms.NumberInput(attrs={'class': 'form-input'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'slug', 'description', 'short_description',
                  'image', 'technologies', 'github_url', 'live_url',
                  'status', 'is_featured', 'order']
        widgets = {
            'title':             forms.TextInput(attrs={'class': 'form-input'}),
            'slug':              forms.TextInput(attrs={'class': 'form-input'}),
            'description':       forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'short_description': forms.TextInput(attrs={'class': 'form-input'}),
            'github_url':        forms.URLInput(attrs={'class': 'form-input'}),
            'live_url':          forms.URLInput(attrs={'class': 'form-input'}),
            'status':            forms.Select(attrs={'class': 'form-input'}),
            'is_featured':       forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'order':             forms.NumberInput(attrs={'class': 'form-input'}),
            'technologies':      forms.CheckboxSelectMultiple(),
        }


class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['name', 'color']
        widgets = {
            'name':  forms.TextInput(attrs={'class': 'form-input'}),
            'color': forms.TextInput(attrs={'class': 'form-input', 'type': 'color'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'field_of_study',
                  'start_year', 'end_year', 'description', 'order']
        widgets = {
            'institution':    forms.TextInput(attrs={'class': 'form-input'}),
            'degree':         forms.TextInput(attrs={'class': 'form-input'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-input'}),
            'start_year':     forms.NumberInput(attrs={'class': 'form-input'}),
            'end_year':       forms.NumberInput(attrs={'class': 'form-input'}),
            'description':    forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'order':          forms.NumberInput(attrs={'class': 'form-input'}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'role', 'start_date', 'end_date',
                  'is_current', 'description', 'order']
        widgets = {
            'company':     forms.TextInput(attrs={'class': 'form-input'}),
            'role':        forms.TextInput(attrs={'class': 'form-input'}),
            'start_date':  forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date':    forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'is_current':  forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'order':       forms.NumberInput(attrs={'class': 'form-input'}),
        }


# ── Views ─────────────────────────────────────────────────────────

@login_required
@admin_required
def dashboard_home(request):
    stats = {
        'projects':  Project.objects.count(),
        'skills':    Skill.objects.count(),
        'messages':  Message.objects.count(),
        'new_msgs':  Message.objects.filter(status='new').count(),
        'users':     User.objects.count(),
        'techs':     Technology.objects.count(),
    }
    recent_messages = Message.objects.order_by('-created_at')[:5]
    recent_projects = Project.objects.order_by('-created_at')[:4]
    context = {'stats': stats, 'recent_messages': recent_messages,
                'recent_projects': recent_projects}
    return render(request, 'dashboard/home.html', context)


# ── Profile ───────────────────────────────────────────────────────

@login_required
@admin_required
def profile_edit(request):
    profile = Profile.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'dashboard/profile.html', {'form': form, 'profile': profile})


# ── Skills ────────────────────────────────────────────────────────

@login_required
@admin_required
def skill_list(request):
    skills = Skill.objects.all()
    return render(request, 'dashboard/skills.html', {'skills': skills})

@login_required
@admin_required
def skill_add(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill added!')
            return redirect('dashboard_skills')
    else:
        form = SkillForm()
    return render(request, 'dashboard/skill_form.html', {'form': form, 'action': 'Add'})

@login_required
@admin_required
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated!')
            return redirect('dashboard_skills')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'dashboard/skill_form.html', {'form': form, 'action': 'Edit', 'skill': skill})

@login_required
@admin_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted!')
    return redirect('dashboard_skills')


# ── Projects ──────────────────────────────────────────────────────

@login_required
@admin_required
def project_list(request):
    projects = Project.objects.prefetch_related('technologies').all()
    return render(request, 'dashboard/projects.html', {'projects': projects})

@login_required
@admin_required
def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            if not project.slug:
                project.slug = slugify(project.title)
            project.save()
            form.save_m2m()
            messages.success(request, 'Project added!')
            return redirect('dashboard_projects')
    else:
        form = ProjectForm()
    techs = Technology.objects.all()
    return render(request, 'dashboard/project_form.html',
                  {'form': form, 'action': 'Add', 'techs': techs})

@login_required
@admin_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated!')
            return redirect('dashboard_projects')
    else:
        form = ProjectForm(instance=project)
    techs = Technology.objects.all()
    return render(request, 'dashboard/project_form.html',
                  {'form': form, 'action': 'Edit', 'project': project, 'techs': techs})

@login_required
@admin_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted!')
    return redirect('dashboard_projects')


# ── Technologies ──────────────────────────────────────────────────

@login_required
@admin_required
def tech_list(request):
    techs = Technology.objects.all()
    return render(request, 'dashboard/technologies.html', {'techs': techs})

@login_required
@admin_required
def tech_add(request):
    if request.method == 'POST':
        form = TechnologyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Technology added!')
            return redirect('dashboard_technologies')
    else:
        form = TechnologyForm()
    return render(request, 'dashboard/tech_form.html', {'form': form, 'action': 'Add'})

@login_required
@admin_required
def tech_edit(request, pk):
    tech = get_object_or_404(Technology, pk=pk)
    if request.method == 'POST':
        form = TechnologyForm(request.POST, instance=tech)
        if form.is_valid():
            form.save()
            messages.success(request, 'Technology updated!')
            return redirect('dashboard_technologies')
    else:
        form = TechnologyForm(instance=tech)
    return render(request, 'dashboard/tech_form.html',
                  {'form': form, 'action': 'Edit', 'tech': tech})

@login_required
@admin_required
def tech_delete(request, pk):
    tech = get_object_or_404(Technology, pk=pk)
    if request.method == 'POST':
        tech.delete()
        messages.success(request, 'Technology deleted!')
    return redirect('dashboard_technologies')


# ── Education ─────────────────────────────────────────────────────

@login_required
@admin_required
def education_list(request):
    educations = Education.objects.all()
    return render(request, 'dashboard/education.html', {'educations': educations})

@login_required
@admin_required
def education_add(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Education added!')
            return redirect('dashboard_education')
    else:
        form = EducationForm()
    return render(request, 'dashboard/education_form.html', {'form': form, 'action': 'Add'})

@login_required
@admin_required
def education_edit(request, pk):
    edu = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=edu)
        if form.is_valid():
            form.save()
            messages.success(request, 'Education updated!')
            return redirect('dashboard_education')
    else:
        form = EducationForm(instance=edu)
    return render(request, 'dashboard/education_form.html',
                  {'form': form, 'action': 'Edit', 'edu': edu})

@login_required
@admin_required
def education_delete(request, pk):
    edu = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        edu.delete()
        messages.success(request, 'Education deleted!')
    return redirect('dashboard_education')


# ── Experience ────────────────────────────────────────────────────

@login_required
@admin_required
def experience_list(request):
    experiences = Experience.objects.all()
    return render(request, 'dashboard/experience.html', {'experiences': experiences})

@login_required
@admin_required
def experience_add(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experience added!')
            return redirect('dashboard_experience')
    else:
        form = ExperienceForm()
    return render(request, 'dashboard/experience_form.html', {'form': form, 'action': 'Add'})

@login_required
@admin_required
def experience_edit(request, pk):
    exp = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experience updated!')
            return redirect('dashboard_experience')
    else:
        form = ExperienceForm(instance=exp)
    return render(request, 'dashboard/experience_form.html',
                  {'form': form, 'action': 'Edit', 'exp': exp})

@login_required
@admin_required
def experience_delete(request, pk):
    exp = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        exp.delete()
        messages.success(request, 'Experience deleted!')
    return redirect('dashboard_experience')


# ── Messages ──────────────────────────────────────────────────────

@login_required
@admin_required
def message_list(request):
    status_filter = request.GET.get('status', '')
    msgs = Message.objects.select_related('user').all()
    if status_filter:
        msgs = msgs.filter(status=status_filter)
    return render(request, 'dashboard/messages.html',
                  {'messages_list': msgs, 'status_filter': status_filter})

@login_required
@admin_required
def message_detail(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if msg.status == 'new':
        msg.status = 'read'
        msg.save()
    return render(request, 'dashboard/message_detail.html', {'msg': msg})

@login_required
@admin_required
def message_status(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    new_status = request.POST.get('status')
    if new_status in ['new', 'read', 'replied', 'archived']:
        msg.status = new_status
        msg.save()
        messages.success(request, f'Message marked as {new_status}.')
    return redirect('dashboard_messages')

@login_required
@admin_required
def message_delete(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Message deleted!')
    return redirect('dashboard_messages')


# ── Users ─────────────────────────────────────────────────────────

@login_required
@admin_required
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/users.html', {'users': users})

@login_required
@admin_required
def user_toggle_staff(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST' and user != request.user:
        user.is_staff = not user.is_staff
        user.save()
        messages.success(request, f"{'Staff access granted to' if user.is_staff else 'Staff access removed from'} {user.username}.")
    return redirect('dashboard_users')