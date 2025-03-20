from django.urls import path, include
from plays import views

app_name = 'plays'

urlpatterns = [
    path('', views.shows, name='shows'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('maps/', views.maps, name='maps'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('<slug:play_slug>/chosen_play/', views.chosen_show, name='choosen_show'),
    path('<slug:play_slug>/review/', views.make_a_review_discuss_event, name='make_a_review_discuss_event'),
    path('submit-rating/', views.submit_rating, name='submit_rating'),

]
