import traceback
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Play, Review, CustomUser, Category
from .forms import ReviewForm
from django.core.exceptions import ObjectDoesNotExist


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

def make_a_review_discuss_event(request, play_slug):
    play = get_object_or_404(Play, slug=play_slug)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, prefix="review")

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.play = play
            review.save()
        
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"message": "Review submitted successfully!"})

            messages.success(request, "Review submitted successfully!")
            return redirect('plays:choosen_show', play_slug=play.slug)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"error": "Invalid data"}, status=400)

            messages.error(request, "Error submitting your review. Please check the form.")
    
    return redirect('plays:choosen_play', play_slug=play.slug)


def about(request):
    return render(request, 'plays/about.html')

def soundtrack(request):
    return render(request, 'plays/soundtrack.html')

def feedback(request):
    return render(request, 'plays/feedback.html')

def maps(request):
    return render(request, 'plays/maps.html')

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
    user_review=None
    ##user_review = Review.objects.filter(playId=play, username=request.user).first()
    
    if request.method == 'POST':  
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.playId = play
            review.save()

            messages.success(request, "Review submitted successfully!")
            return redirect('plays:choosen_plays', play_slug=play.slug)  
        
        messages.error(request, "Error submitting review.")

    else:
        review_form = ReviewForm()

    context = {
        'play': play,
        'user_review': user_review,
        'review_form': review_form
    }
    return render(request, 'plays/chosen_show.html', context)


def submit_rating(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        play_id = request.POST.get('el_id')  
        rating_value = request.POST.get('val') 
        category = request.POST.get('category')  

        if not play_id or not rating_value or not category:
            return JsonResponse({'error': 'Missing data'}, status=400)
        try:
            rating_value = int(rating_value)
        except ValueError:
            return JsonResponse({'error': 'Invalid rating value'}, status=400)

        if category not in ['soundtrack', 'set', 'cast']:
            return JsonResponse({'error': 'Invalid rating category'}, status=400)


        # getting the play
        play = get_object_or_404(Play, playID=play_id)

        review, created = Review.objects.get_or_create(
            playId=play, username=request.user,
            defaults={'SoundTrackRating': 1, 'CastRating': 1, 'SetRating': 1, 'AverageRating': 1}
        )

        if category == 'soundtrack':
            review.SoundTrackRating = rating_value
        elif category == 'set':
            review.SetRating = rating_value
        elif category == 'cast':
            review.CastRating = rating_value

        #this is calculating the averaeg rating 
        total_ratings = sum(filter(None, [review.SoundTrackRating, review.CastRating, review.SetRating]))
        count = sum(1 for x in [review.SoundTrackRating, review.CastRating, review.SetRating] if x > 0)
        review.AverageRating = total_ratings // count if count else 0

        review.save()

        return JsonResponse({'message': 'Rating submitted successfully!', 'score': rating_value})

    return JsonResponse({'error': 'Invalid request'}, status=400)