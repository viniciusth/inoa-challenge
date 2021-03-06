"""tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from assets.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name = 'home'),
    path('login/', login_view, name = 'login'),
    path('register/', register_view, name = 'register'),
    path('profile/', profile_view, name = 'profile'),
    path('logout/', logout_view, name = 'logout'),
    path('profile/edit/', edit_user_view, name = 'edit_user'),
    path('profile/change_password/', change_password_view, name = 'change_password'),
    path('profile/assets/', assets_view, name = 'assets'),
    path('profile/assets/add', asset_add_view, name ='asset_add'),
    path('profile/assets/remove', asset_remove_view, name ='asset_remove'),
    path('assets/', all_assets_view, name = 'all_assets'),
    path('assets/<str:ticker>/', some_asset_view, name = 'some_asset'),
]
