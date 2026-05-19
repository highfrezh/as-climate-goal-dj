from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('author/<slug:slug>/', views.author_detail, name='author_detail'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('contact/', views.contact_view, name='contact'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard Home
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Research Resources CRUD
    path('dashboard/research/', views.manage_research, name='manage_research'),
    path('dashboard/research/edit/<int:pk>/', views.manage_research, name='edit_research'),
    path('dashboard/research/delete/<int:pk>/', views.delete_research, name='delete_research'),
    
    # Climate Articles CRUD (Videos)
    path('dashboard/articles/', views.manage_climate_articles, name='manage_climate_articles'),
    path('dashboard/articles/create/', views.create_climate_article, name='create_climate_article'),
    path('dashboard/articles/edit/<int:pk>/', views.edit_climate_article, name='edit_climate_article'),
    path('dashboard/articles/delete/<int:pk>/', views.delete_climate_article, name='delete_climate_article'),
    
    # Authors CRUD
    path('dashboard/authors/', views.manage_authors, name='manage_authors'),
    path('dashboard/authors/edit/<int:pk>/', views.manage_authors, name='edit_author'),
    path('dashboard/authors/delete/<int:pk>/', views.delete_author, name='delete_author'),
    
    # Settings CRUD (Includes Founder)
    path('dashboard/settings/', views.manage_settings, name='manage_settings'),
    
    # User Management
    path('dashboard/users/', views.manage_users, name='manage_users'),
    path('dashboard/users/edit/<int:pk>/', views.manage_users, name='edit_user'),
    path('dashboard/users/password/<int:pk>/', views.reset_password, name='reset_password'),
    path('dashboard/users/delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('dashboard/users/<int:pk>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    
    # Newsletter Subscribers
    path('dashboard/subscribers/', views.manage_subscribers, name='manage_subscribers'),
    path('dashboard/subscribers/delete/<int:pk>/', views.delete_subscriber, name='delete_subscriber'),
    
    # Dashboard Inbox
    path('dashboard/inbox/', views.manage_inbox, name='manage_inbox'),
    path('dashboard/inbox/delete/<int:pk>/', views.delete_message, name='delete_message'),
]
