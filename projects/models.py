from django.db import models
from cloudinary.models import CloudinaryField


class Technology(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#6366f1', help_text='Hex color for tag badge')

    class Meta:
        verbose_name_plural = 'Technologies'
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('live', 'Live'),
        ('development', 'In Development'),
        ('archived', 'Archived'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    image = CloudinaryField('image')
    technologies = models.ManyToManyField(Technology, blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='live')
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
