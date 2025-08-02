"""
URL configuration for LibraryProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    # ===============================
    # Django Admin site
    # ===============================
    path('admin/', admin.site.urls),
    # This route gives access to Django's built-in admin interface.

    # ===============================
    # App routes
    # ===============================
    path('relationship_app/', include('relationship_app.urls')),
    # Includes all URLs from the relationship_app's urls.py
    # Any URL starting with /relationship_app/ will be handled there.

    # ===============================
    # Authentication routes
    # ===============================
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # This is Django's built-in login view.
    # The 'accounts/login/' path is used by Django's authentication system
    # as the default redirect when a user is not logged in and tries to
    # access a protected view (@login_required or @user_passes_test).
    #
    # Why 'accounts'?
    # - It's the default convention in Django for auth routes.
    # - The built-in logout view is also found at 'accounts/logout/' if configured.
    # - You can change this path, but using 'accounts/' keeps compatibility
    #   with Django's default redirects.
]
