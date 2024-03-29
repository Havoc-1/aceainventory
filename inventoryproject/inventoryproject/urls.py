"""inventoryproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from user import views as user_view
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static      #allow to set url patterns to import static
from django.conf import settings                #import var from settings


urlpatterns = [
    # everytime the first '' is called, the following views are called
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('register/', user_view.register, name='user-register'),
    path('', user_view.customLoginView.as_view(), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
    path('profile/', user_view.view_profile, name='view-profile'),
    path('profile/edit/', user_view.edit_profile, name='edit-profile'),
    path('profile/password/', user_view.change_password, name='password'),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT) #auto create URL to reference images
