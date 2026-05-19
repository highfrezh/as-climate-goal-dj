from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from .models import ResearchResources, ClimateArticles, Author, SiteSettings, Founder

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'role', 'photo', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'rich-editor'}),
            'photo': forms.FileInput(),
        }

class ResearchResourcesForm(forms.ModelForm):
    class Meta:
        model = ResearchResources
        fields = ['title', 'description', 'external_url', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ClimateArticlesForm(forms.ModelForm):
    class Meta:
        model = ClimateArticles
        fields = ['title', 'description', 'content', 'category', 'status', 'date', 'author', 'video_url', 'custom_thumbnail', 'pdf_report', 'is_featured']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'rich-editor'}),
            'custom_thumbnail': forms.FileInput(),
            'pdf_report': forms.FileInput(),
        }

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'hero_subtitle': forms.Textarea(attrs={'rows': 2}),
            'intro_description': forms.Textarea(attrs={'rows': 3}),
            'vision': forms.Textarea(attrs={'rows': 2}),
            'mission': forms.Textarea(attrs={'rows': 2}),
            'values': forms.Textarea(attrs={'rows': 2}),
            'logo': forms.FileInput(),
            'favicon': forms.FileInput(),
            'hero_image': forms.FileInput(),
            'hero_video': forms.FileInput(),
            'intro_image': forms.FileInput(),
            'privacy_policy': forms.Textarea(attrs={'rows': 10, 'class': 'rich-editor'}),
        }

class FounderForm(forms.ModelForm):
    class Meta:
        model = Founder
        fields = '__all__'
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'rich-editor'}),
            'photo': forms.FileInput(),
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
