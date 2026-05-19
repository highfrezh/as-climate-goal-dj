from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import ResearchResources, ClimateArticles, Author, SiteSettings, Founder, Subscriber, ContactMessage
from .forms import ResearchResourcesForm, ClimateArticlesForm, AuthorForm, SiteSettingsForm, FounderForm, UserEditForm

def index(request):
    research_links_qs = ResearchResources.objects.all().order_by('-date')
    research_paginator = Paginator(research_links_qs, 6)
    rpage_number = request.GET.get('rpage')
    research_page_obj = research_paginator.get_page(rpage_number)

    all_articles = ClimateArticles.objects.filter(status='published').order_by('-is_featured', '-date')
    
    featured_articles = all_articles[:5]
    remaining_articles = all_articles[5:]
    
    paginator = Paginator(remaining_articles, 6)  # 6 articles per page for a 3-column grid
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    authors = Author.objects.all().order_by('name')
    settings = SiteSettings.objects.first()
    founder = Founder.objects.first()
    
    context = {
        'research_links': research_page_obj.object_list,
        'research_page_obj': research_page_obj,
        'all_articles': all_articles,  # keep for backward compatibility if needed, though we will use featured_articles and page_obj
        'featured_articles': featured_articles,
        'page_obj': page_obj,
        'authors': authors,
        'settings': settings,
        'founder': founder,
    }
    return render(request, 'articles/index.html', context)

def article_detail(request, slug):
    article = get_object_or_404(ClimateArticles, slug=slug, status='published')
    
    # Related articles by the same author (excluding current, up to 3)
    related_articles = ClimateArticles.objects.filter(
        author=article.author, 
        status='published'
    ).exclude(pk=article.pk).order_by('-date')[:3]
    
    # Recommended featured articles (excluding current, up to 4)
    recommended_qs = ClimateArticles.objects.filter(
        is_featured=True, 
        status='published'
    ).exclude(pk=article.pk).order_by('-date')[:4]
    
    # Evaluate queryset to list to avoid MySQL "LIMIT & IN" subquery limitations
    recommended_list = list(recommended_qs)
    recommended_ids = [a.pk for a in recommended_list]
    
    # Fallback to general articles if fewer than 4 featured articles are available
    if len(recommended_list) < 4:
        needed = 4 - len(recommended_list)
        additional = ClimateArticles.objects.filter(
            status='published'
        ).exclude(pk=article.pk).exclude(pk__in=recommended_ids).order_by('-date')[:needed]
        recommended_articles = recommended_list + list(additional)
    else:
        recommended_articles = recommended_list
    
    settings = SiteSettings.objects.first()
    
    context = {
        'article': article,
        'settings': settings,
        'related_articles': related_articles,
        'recommended_articles': recommended_articles[:4],
    }
    return render(request, 'articles/article_detail.html', context)

def author_detail(request, slug):
    author = get_object_or_404(Author, slug=slug)
    articles = author.articles.filter(status='published').order_by('-date')
    settings = SiteSettings.objects.first()
    return render(request, 'articles/author_detail.html', {
        'author': author, 
        'articles': articles,
        'settings': settings
    })

# --- DASHBOARD VIEWS ---

@staff_member_required(login_url='login')
def dashboard(request):
    context = {
        'total_research': ResearchResources.objects.count(),
        'total_videos': ClimateArticles.objects.count(),
        'total_authors': Author.objects.count(),
        'total_users': User.objects.count(),
        'total_subscribers': Subscriber.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'recent_articles': ClimateArticles.objects.order_by('-date')[:5],
        'settings': SiteSettings.objects.first(),
    }
    return render(request, 'articles/dashboard/home.html', context)

# 1. Research Resources CRUD
@staff_member_required(login_url='login')
def manage_research(request, pk=None):
    items_list = ResearchResources.objects.all().order_by('-created_at')
    instance = get_object_or_404(ResearchResources, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = ResearchResourcesForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('manage_research')
    else:
        form = ResearchResourcesForm(instance=instance)
    
    paginator = Paginator(items_list, 5)
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)
    
    return render(request, 'articles/dashboard/research.html', {
        'items': items, 
        'form': form, 
        'edit_mode': bool(pk)
    })

@staff_member_required(login_url='login')
def delete_research(request, pk):
    get_object_or_404(ResearchResources, pk=pk).delete()
    return redirect('manage_research')

# 2. Climate Articles CRUD (Videos)
from django.core.paginator import Paginator
from django.db.models import Q

@staff_member_required(login_url='login')
def manage_climate_articles(request):
    query = request.GET.get('q')
    articles_list = ClimateArticles.objects.all().order_by('-date')
    
    if query:
        articles_list = articles_list.filter(
            Q(title__icontains=query) | 
            Q(author__name__icontains=query) |
            Q(description__icontains=query)
        )
    
    featured_count = ClimateArticles.objects.filter(is_featured=True).count()
    author_count = ClimateArticles.objects.values('author').distinct().count()
    
    paginator = Paginator(articles_list, 10) # 10 articles per page
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    context = {
        'articles': articles,
        'featured_count': featured_count,
        'author_count': author_count,
        'query': query,
    }
    return render(request, 'articles/dashboard/climate_articles.html', context)

@staff_member_required(login_url='login')
def create_climate_article(request):
    if request.method == 'POST':
        form = ClimateArticlesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_climate_articles')
    else:
        form = ClimateArticlesForm()
    return render(request, 'articles/dashboard/create_edit_article.html', {'form': form})

@staff_member_required(login_url='login')
def edit_climate_article(request, pk):
    article = get_object_or_404(ClimateArticles, pk=pk)
    if request.method == 'POST':
        form = ClimateArticlesForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('manage_climate_articles')
    else:
        form = ClimateArticlesForm(instance=article)
    return render(request, 'articles/dashboard/create_edit_article.html', {'form': form, 'edit_mode': True})

@staff_member_required(login_url='login')
def delete_climate_article(request, pk):
    get_object_or_404(ClimateArticles, pk=pk).delete()
    return redirect('manage_climate_articles')

# 3. Authors CRUD
@staff_member_required(login_url='login')
def manage_authors(request, pk=None):
    authors = Author.objects.all().order_by('name')
    instance = get_object_or_404(Author, pk=pk) if pk else None
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('manage_authors')
    else:
        form = AuthorForm(instance=instance)
    return render(request, 'articles/dashboard/authors.html', {'authors': authors, 'form': form, 'edit_mode': bool(pk)})

@staff_member_required(login_url='login')
def delete_author(request, pk):
    get_object_or_404(Author, pk=pk).delete()
    return redirect('manage_authors')

# 4. Global Settings & About
@staff_member_required(login_url='login')
def manage_settings(request):
    settings = SiteSettings.objects.first() or SiteSettings.objects.create()
    founder = Founder.objects.first() or Founder.objects.create()
    if request.method == 'POST':
        if 'settings_form' in request.POST:
            form = SiteSettingsForm(request.POST, request.FILES, instance=settings)
            if form.is_valid(): form.save()
        elif 'founder_form' in request.POST:
            form = FounderForm(request.POST, request.FILES, instance=founder)
            if form.is_valid(): form.save()
        return redirect('manage_settings')
    return render(request, 'articles/dashboard/settings.html', {
        'settings': settings,
        'founder': founder,
        'settings_form': SiteSettingsForm(instance=settings),
        'founder_form': FounderForm(instance=founder),
    })

# 5. User Management
@staff_member_required(login_url='login')
def manage_users(request, pk=None):
    if not request.user.is_superuser: return redirect('dashboard')
    users = User.objects.all().order_by('-date_joined')
    instance = get_object_or_404(User, pk=pk) if pk else None
    if request.method == 'POST':
        if pk:
            form = UserEditForm(request.POST, instance=instance)
            if form.is_valid(): form.save(); return redirect('manage_users')
        else:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                new_user.is_staff = True
                new_user.is_superuser = True
                new_user.save()
                return redirect('manage_users')
    else:
        form = UserEditForm(instance=instance) if pk else UserCreationForm()
    return render(request, 'articles/dashboard/users.html', {'users': users, 'form': form, 'edit_mode': bool(pk), 'edit_user': instance})

@staff_member_required(login_url='login')
def reset_password(request, pk):
    if not request.user.is_superuser: return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid(): form.save(); return redirect('manage_users')
    else:
        form = SetPasswordForm(user)
    return render(request, 'articles/dashboard/reset_password.html', {'form': form, 'target_user': user})

@staff_member_required(login_url='login')
def delete_user(request, pk):
    if not request.user.is_superuser: return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    if user != request.user: user.delete()
    return redirect('manage_users')

# --- AUTH ---

def login_view(request):
    if request.user.is_authenticated: return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next', 'dashboard'))
    else:
        form = AuthenticationForm()
    return render(request, 'articles/auth/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('index')
@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_user_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f"Status for {user.username} updated successfully.")
    else:
        messages.error(request, "You cannot deactivate your own account.")
    return redirect('manage_users')

# --- NEWSLETTER ---
def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                Subscriber.objects.create(email=email)
                messages.success(request, "Thank you! You've successfully subscribed to our newsletter.")
            except IntegrityError:
                messages.info(request, "You are already subscribed to our newsletter!")
        else:
            messages.error(request, "Please provide a valid email address.")
    
    # Redirect back to the page the user came from, or index as fallback
    referer = request.META.get('HTTP_REFERER')
    if referer:
        if '#' in referer:
            referer = referer.split('#')[0]
        return redirect(f"{referer}#newsletter")
    return redirect('/#newsletter')

@staff_member_required(login_url='login')
def manage_subscribers(request):
    subscribers_list = Subscriber.objects.all().order_by('-subscribed_at')
    paginator = Paginator(subscribers_list, 10)
    page_number = request.GET.get('page')
    subscribers = paginator.get_page(page_number)
    return render(request, 'articles/dashboard/subscribers.html', {'subscribers': subscribers})

@staff_member_required(login_url='login')
def delete_subscriber(request, pk):
    subscriber = get_object_or_404(Subscriber, pk=pk)
    subscriber.delete()
    messages.success(request, "Subscriber removed successfully.")
    return redirect('manage_subscribers')

def privacy_policy(request):
    settings = SiteSettings.objects.first()
    return render(request, 'articles/privacy_policy.html', {'settings': settings})

def contact_view(request):
    settings = SiteSettings.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, "Your message has been sent successfully! We will get back to you soon.")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all fields.")
    return render(request, 'articles/contact.html', {'settings': settings})

@staff_member_required(login_url='login')
def manage_inbox(request):
    read_id = request.GET.get('read_id')
    if read_id:
        msg = get_object_or_404(ContactMessage, pk=read_id)
        msg.is_read = True
        msg.save()
        return redirect('manage_inbox')
        
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter == 'unread':
        messages_list = messages_list.filter(is_read=False)
    elif status_filter == 'read':
        messages_list = messages_list.filter(is_read=True)

    paginator = Paginator(messages_list, 10)
    page_number = request.GET.get('page')
    inbox_messages = paginator.get_page(page_number)
    return render(request, 'articles/dashboard/inbox.html', {
        'inbox_messages': inbox_messages,
        'status_filter': status_filter or 'all'
    })

@staff_member_required(login_url='login')
def delete_message(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    messages.success(request, "Message deleted successfully.")
    return redirect('manage_inbox')
