from django.contrib import admin
from .models import Project, Technology


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_featured', 'order', 'created_at']
    list_filter = ['status', 'is_featured', 'technologies']
    list_editable = ['order', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    search_fields = ['title', 'description']
