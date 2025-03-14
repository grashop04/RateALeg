from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Play, Review, CustomUser, Category
from .forms import ReviewForm

def shows(request):
    category_name = request.GET.get('category')
    sort_by = request.GET.get('sort', 'title')  
    
    if category_name:
        plays = Play.objects.filter(genre=category_name)
    else:
        plays = Play.objects.all()
    
    if sort_by == 'rating':
        plays = plays.order_by('-rating')
    elif sort_by == 'playwright':
        plays = plays.order_by('WriterFirstName', 'WriterSecondName')
    elif sort_by == 'newest':
        plays = plays.order_by('-releaseDate')
    else:
        plays = plays.order_by('title')
    
    categories = Category.objects.all()
    return render(request, 'plays/shows.html', {'plays': plays, 'categories': categories, 'sort_by': sort_by})

def show_detail(request, show_id):
    play = get_object_or_404(Play, id=show_id)
    reviews = play.reviews.all()
    return render(request, 'plays/show_detail.html', {'play': play, 'reviews': reviews})

@login_required
def add_review(request, show_id):
    play = get_object_or_404(Play, id=show_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.play = play
            review.save()
            return redirect('plays:show_detail', show_id=play.id)
    else:
        form = ReviewForm()
    return render(request, 'plays/add_review.html', {'form': form, 'play': play})

def about(request):
    return render(request, 'plays/about.html')

def soundtrack(request):
    return render(request, 'plays/soundtrack.html')

def feedback(request):
    return render(request, 'plays/feedback.html')

def maps(request):
    context_dict = {}
    context_dict['kingstheatre'] = 'http://kingstheatreglasgow.net/'
    context_dict['theatreroyal'] = 'http://theatreroyalglasgow.net/'
    context_dict['paviliontheatre'] = 'https://trafalgartickets.com/pavilion-theatre-glasgow/en-GB'

    
    return render(request, 'plays/maps.html', context_dict)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('plays:show_list')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'plays/login.html')

def logout_view(request):
    logout(request)
    return redirect('plays:login')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        bio = request.POST.get('bio')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = CustomUser.objects.create_user(
                username=username, password=password,
                firstName=first_name, secondName=second_name, bio=bio
            )
            login(request, user)
            return redirect('plays:show_list')
    return render(request, 'plays/signup.html')

@login_required
def profile(request):
    user_profile = get_object_or_404(CustomUser, id=request.user.id)
    return render(request, 'plays/profile.html', {'user_profile': user_profile})

def chosen_show(request, play_slug):
    play = get_object_or_404(Play, slug=play_slug)
    return render(request, 'plays/chosen_show.html', {'play': play})
