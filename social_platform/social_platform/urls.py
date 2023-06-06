"""
URL configuration for social_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from TimeFollow import views as tf_views
from django.contrib.auth import views as auth

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('TimeFollow.urls')),
    path('login/', tf_views.Login, name='login'),
    path('logout/', auth.LogoutView.as_view(template_name = 'TimeFollow/index.html'), name='logout'),
    path('register/', tf_views.register, name='register'),
    path('createPost/', tf_views.CreatePost, name='createpost'),
    path('timeline/', tf_views.ViewTimeline, name='timeline'),
]