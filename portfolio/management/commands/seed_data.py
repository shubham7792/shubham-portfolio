"""
Management command to populate the database with demo data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from portfolio.models import Profile, Skill, Education, Experience
from projects.models import Project, Technology
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Seed database with demo portfolio data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Profile
        profile, _ = Profile.objects.get_or_create(
            name='Jace Smith',
            defaults={
                'title': 'Full Stack Developer',
                'tagline': 'Building beautiful & functional digital experiences.',
                'bio': 'I am a passionate Full Stack Developer with 5+ years of experience crafting robust web applications. I specialize in Django, React, and PostgreSQL. I love turning complex problems into elegant, user-friendly solutions and I am always looking for new challenges.',
                'github_url': 'https://github.com',
                'linkedin_url': 'https://linkedin.com',
                'twitter_url': 'https://twitter.com',
                'email': 'jace@example.com',
                'is_active': True,
            }
        )

        # Skills
        skills_data = [
            ('HTML5', 'fab fa-html5', 'frontend', 95),
            ('CSS3', 'fab fa-css3-alt', 'frontend', 90),
            ('JavaScript', 'fab fa-js', 'frontend', 85),
            ('Python', 'fab fa-python', 'backend', 92),
            ('Django', 'fas fa-globe', 'backend', 90),
            ('PostgreSQL', 'fas fa-database', 'backend', 80),
            ('Git', 'fab fa-git-alt', 'tools', 88),
            ('Bootstrap', 'fab fa-bootstrap', 'frontend', 85),
            ('Docker', 'fab fa-docker', 'tools', 70),
            ('Linux', 'fab fa-linux', 'tools', 75),
        ]
        for name, icon, cat, prof in skills_data:
            Skill.objects.get_or_create(name=name, defaults={
                'icon_class': icon, 'category': cat, 'proficiency': prof
            })

        # Education
        Education.objects.get_or_create(
            institution='MIT',
            defaults={
                'degree': 'B.S. Computer Science',
                'field_of_study': 'Computer Science & Engineering',
                'start_year': 2016, 'end_year': 2020,
                'description': 'Focused on software engineering, algorithms, and distributed systems.'
            }
        )

        # Experience
        Experience.objects.get_or_create(
            company='TechCorp Inc.',
            defaults={
                'role': 'Senior Full Stack Developer',
                'start_date': '2021-01-01',
                'is_current': True,
                'description': 'Led development of enterprise SaaS platform serving 50k+ users. Built with Django, React, and PostgreSQL.'
            }
        )
        Experience.objects.get_or_create(
            company='StartupXYZ',
            defaults={
                'role': 'Backend Developer',
                'start_date': '2020-06-01',
                'end_date': '2020-12-31',
                'description': 'Developed REST APIs and microservices using Django REST Framework.'
            }
        )

        # Technologies
        tech_data = [
            ('Django', '#092E20'),
            ('Python', '#3776AB'),
            ('React', '#61DAFB'),
            ('PostgreSQL', '#336791'),
            ('Docker', '#2496ED'),
            ('JavaScript', '#F7DF1E'),
            ('TypeScript', '#3178C6'),
            ('CSS', '#1572B6'),
        ]
        techs = {}
        for name, color in tech_data:
            t, _ = Technology.objects.get_or_create(name=name, defaults={'color': color})
            techs[name] = t

        # Projects
        projects_data = [
            {
                'title': 'E-Commerce Platform',
                'slug': 'ecommerce-platform',
                'description': 'A full-featured e-commerce platform with inventory management, payment processing, and analytics dashboard.',
                'short_description': 'Full-featured e-commerce platform with payment processing and analytics.',
                'github_url': 'https://github.com',
                'live_url': 'https://example.com',
                'status': 'live',
                'is_featured': True,
                'technologies': ['Django', 'Python', 'PostgreSQL', 'JavaScript'],
            },
            {
                'title': 'Task Management App',
                'slug': 'task-management-app',
                'description': 'A collaborative task management application with real-time updates, kanban boards, and team collaboration features.',
                'short_description': 'Collaborative task manager with Kanban boards and real-time updates.',
                'github_url': 'https://github.com',
                'live_url': '',
                'status': 'live',
                'is_featured': False,
                'technologies': ['React', 'Django', 'PostgreSQL'],
            },
            {
                'title': 'Developer Portfolio',
                'slug': 'developer-portfolio',
                'description': 'This portfolio website built with Django, featuring authentication, project showcase, and contact form.',
                'short_description': 'This portfolio website with Django backend and modern frontend.',
                'github_url': 'https://github.com',
                'live_url': 'https://example.com',
                'status': 'live',
                'is_featured': True,
                'technologies': ['Django', 'Python', 'CSS', 'JavaScript'],
            },
        ]
        for pd in projects_data:
            tech_names = pd.pop('technologies')
            project, created = Project.objects.get_or_create(
                slug=pd['slug'],
                defaults=pd
            )
            if created:
                for tn in tech_names:
                    if tn in techs:
                        project.technologies.add(techs[tn])

        self.stdout.write(self.style.SUCCESS('✅ Demo data seeded successfully!'))
        self.stdout.write('Create a superuser: python manage.py createsuperuser')
