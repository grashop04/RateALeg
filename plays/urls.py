from django.urls import path, include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from plays import views

app_name = 'plays'

urlpatterns = [
    path('', views.shows, name='shows'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('maps/', views.maps, name='maps'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('profile/', views.profile, name='profile'),
#    path("profile/edit/", views.update_profile, name="update_profile"),
    path('search/', views.search, name='search'),
    path('<slug:play_slug>/chosen_play/', views.chosen_show, name='chosen_show'),
    path('logout/', views.user_logout, name="logout"),
    path('<slug:play_slug>/review/', views.make_a_review_discuss_event, name='make_a_review_discuss_event'),
    path('submit-rating/', views.submit_rating, name='submit_rating'),
    path('submit-comment/', views.submit_comment, name='submit_comment'),
    path('top-rated/', views.top_rated, name='top_rated'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)