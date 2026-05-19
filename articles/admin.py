from django.contrib import admin
from .models import ResearchResources, ClimateArticles, Author, SiteSettings, Founder

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ('name',)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not Founder.objects.exists()

@admin.register(ResearchResources)
class ResearchResourcesAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)

@admin.register(ClimateArticles)
class ClimateArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_featured', 'date')
    list_filter = ('is_featured', 'date', 'author')
    search_fields = ('title', 'author__name')
