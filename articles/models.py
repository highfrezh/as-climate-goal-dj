import os
import re
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

class SiteSettings(models.Model):
    hero_title = models.CharField(max_length=255, default="Welcome to Alimat Sustainability Climate Goal")
    hero_subtitle = models.TextField(default="Empowering the next generation with the knowledge and tools to drive climate resilience across Africa.")
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True)
    hero_video = models.FileField(upload_to='site/', blank=True, null=True, help_text="Upload an MP4 video to use as the hero background.")
    
    intro_title = models.CharField(max_length=255, default="Introduction to Climate Change in Africa")
    intro_description = models.TextField(default="Climate change is not just a global issue — it’s a story that affects every home, business, and community in Africa.")
    intro_image = models.ImageField(upload_to='site/', blank=True, null=True)
    
    vision = models.TextField(default="A climate-resilient Africa built on education and sustainable action.")
    mission = models.TextField(default="To raise awareness and drive climate action through learning, creativity, and youth empowerment.")
    values = models.TextField(default="Education | Inclusion | Sustainability | Innovation | Community")
    
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    privacy_policy = models.TextField(blank=True, default="<h2>Privacy Policy</h2><p>Your privacy policy content goes here...</p>")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

class Founder(models.Model):
    name = models.CharField(max_length=100, default="Mrs Alimat Oladipupo Jinadu S.")
    role = models.CharField(max_length=100, default="Founder")
    bio = models.TextField()
    photo = models.ImageField(upload_to='founder/', blank=True, null=True)

class Author(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True, help_text="A short biography of the author.")
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50].rstrip('-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ResearchResources(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    external_url = models.URLField()
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Research Resource"
        verbose_name_plural = "Research Resources"

    def __str__(self):
        return self.title

class ClimateArticles(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    content = models.TextField(blank=True, help_text="Write your full article content here.")
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    
    PLATFORM_CHOICES = [
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
    ]
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES, default='tiktok')
    
    category = models.CharField(max_length=100, default="Video Insights")
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, related_name='articles')
    
    video_url = models.URLField(blank=True, help_text="Paste your TikTok or YouTube link here")
    video_id = models.CharField(max_length=100, blank=True)
    custom_thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    pdf_report = models.FileField(upload_to='reports/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Climate Article"
        verbose_name_plural = "Climate Articles"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50].rstrip('-')
            
        if self.video_url:
            # 1. YouTube Extraction
            youtube_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', self.video_url)
            if youtube_match:
                self.video_id = youtube_match.group(1)
                self.platform = 'youtube'
            
            # 2. TikTok Extraction
            tiktok_match = re.search(r'video/(\d+)', self.video_url)
            if tiktok_match:
                self.video_id = tiktok_match.group(1)
                self.platform = 'tiktok'
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.subject} - {self.name}"

# --- AUTO CLEANUP SIGNALS ---

@receiver(post_delete)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if isinstance(field, models.FileField) or isinstance(field, models.ImageField):
            try:
                file = getattr(instance, field.name)
                if file and os.path.isfile(file.path):
                    os.remove(file.path)
            except (ValueError, FileNotFoundError): pass

@receiver(pre_save)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk: return False
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist: return False

    for field in instance._meta.fields:
        if isinstance(field, models.FileField) or isinstance(field, models.ImageField):
            try:
                old_file = getattr(old_instance, field.name)
                new_file = getattr(instance, field.name)
                if old_file and old_file != new_file:
                    if os.path.isfile(old_file.path):
                        os.remove(old_file.path)
            except (ValueError, FileNotFoundError): pass
