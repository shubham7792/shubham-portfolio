from django.db import models
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    name = models.CharField(max_length=100, default='Jace Smith')
    title = models.CharField(max_length=100, default='Full Stack Developer')
    tagline = models.CharField(max_length=200, default='Building beautiful & functional digital experiences.')
    bio = models.TextField(blank=True)
    profile_image = CloudinaryField('image', blank=True, null=True)
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('tools', 'Tools & DevOps'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=100, blank=True, help_text='FontAwesome class e.g. fab fa-python')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    proficiency = models.IntegerField(default=80, help_text='0-100 percentage')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-start_year']

    def __str__(self):
        return f'{self.degree} - {self.institution}'


class Experience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.role} at {self.company}'
