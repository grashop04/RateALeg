"""rate_a_leg_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from plays import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.shows, name='shows'),
    path('plays/', include('plays.urls')),
    path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('maps/', views.maps, name='maps'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('feedback/', views.feedback, name='feedback'),
    path('logout/', views.logout, name='logout'),
    path('<slug:play_slug>/chosen_show/', views.chosen_show, name='chosen_show'),
    path('logout/', views.user_logout, name="logout"),
    path('submit-rating/', views.submit_rating, name='submit-rating'),
    path('submit-comment/', views.submit_comment, name='submit_comment'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
