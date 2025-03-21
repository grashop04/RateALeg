import traceback
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.templatetags.static import static
from .models import Play, Review, CustomUser, Category
from .forms import ReviewForm, ProfileForm
from django.urls import reverse
from .forms import SignUpForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg


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

    try:
        featured_play = Play.objects.get(title="Annie, The Musical")
        if not featured_play.slug:
            featured_play.slug = "annie-the-musical"
            featured_play.save()
    except Play.DoesNotExist:
        featured_play = None
    categories = Category.objects.all()
    return render(request, 'plays/shows.html', {'plays': plays, 'categories': categories, 'sort_by': sort_by, 'featured_play': featured_play,})

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
    context_dict = {}
    context_dict['kingstheatre'] = 'http://kingstheatreglasgow.net/'
    context_dict['theatreroyal'] = 'http://theatreroyalglasgow.net/'
    context_dict['paviliontheatre'] = 'https://trafalgartickets.com/pavilion-theatre-glasgow/en-GB'

    
    return render(request, 'plays/maps.html', context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('shows'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'plays/login.html')

def logout_view(request):
    logout(request)
    return redirect('plays:login')

def user_signup(request):
    registered = False

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            registered = True
            login(request, user)
            return redirect('shows')
        else:
            print(form.errors)
    else:
        form = SignUpForm()

    return render(request, 'plays/signup.html',
                  context={'form': form, 'registered': registered})

@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        if request.content_type == "application/json":
            data = json.loads(request.body)
            user.bio = data.get("bio", user.bio)
            user.save()
            return JsonResponse({"success": True})

        elif request.FILES.get("profile_pic"): 
            user.profilePicture = request.FILES["profile_pic"]
            user.save()
            return JsonResponse({"success": True})

        return JsonResponse({"success": False})
    
    profile_picture_url = user.profilePicture.url if user.profilePicture else static("images/default-profile-pic.jpg")
    return render(request, "plays/profile.html", {"user": user, "profile_picture_url": profile_picture_url})



@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('shows'))

def chosen_show(request, play_slug):
    play = get_object_or_404(Play, slug=play_slug)
    user_review=None
    ##user_review = Review.objects.filter(playId=play, username=request.user).first()
    user_has_reviewed = False
    
    if request.user.is_authenticated:
        user_review = Review.objects.filter(playId=play, username=request.user).first()
        user_has_reviewed = user_review is not None


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


    avg_rating = Review.objects.filter(playId=play).aggregate(Avg('AverageRating'))['AverageRating__avg']
    
    if avg_rating is None:
        avg_rating = 0  
    else:
        avg_rating = round(avg_rating, 1)  

    context = {
        'play': play,
        'user_review': user_review,
        'review_form': review_form,
        'avg_rating':avg_rating,
        'user_has_reviewed': user_has_reviewed,
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
         except (TypeError, ValueError):
            return JsonResponse({'error': 'Invalid rating value'}, status=400)

         if category not in ['soundtrack', 'set', 'cast']:
            return JsonResponse({'error': 'Invalid rating category'}, status=400)

         play = get_object_or_404(Play, playID=play_id)

         review, created = Review.objects.get_or_create(
         playId=play,
         username=request.user,
        
         defaults={
         'SoundTrackRating': 0,
         'SetRating': 0,
         'CastRating': 0,
         'AverageRating': 0
         }
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