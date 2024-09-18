"""
URL configuration for ecoton project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from main.species.lists import SpeciesListView, SpeciesTypesListView, HabitatAreasListView, FavoriteSpeciesListView
from main.user_info.views import UserInfoView, UserRegistrtionView, UserLoginView
from main.species.detail import DetailSpeciesView, UserFavoritesView, HabitatAreasDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/register', UserRegistrtionView.as_view(), name='user_register'),
    path('user/login', UserLoginView.as_view(), name='user_login'),
    path('user/info', UserInfoView.as_view(), name='user_info'),

    path('species/list', SpeciesListView.as_view(), name='species_list'),
    path('species/types', SpeciesTypesListView.as_view(), name='species_types_list'),
    path('species/detail', DetailSpeciesView.as_view(), name='species_detail'),
    path('species/change_favorite', UserFavoritesView.as_view(), name='change_favorite'),
    path('species/top_favorite', FavoriteSpeciesListView.as_view(), name='favorite_species_list'),

    path('arias/list', HabitatAreasListView.as_view(), name='arias_list'),
    path('arias/detail', HabitatAreasDetailView.as_view(), name='arias_detail'),
]


if settings.DEBUG: 
    urlpatterns += static('media', document_root=settings.MEDIA_ROOT)