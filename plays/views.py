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
    return render(request, 'plays/chosen_show.html', {'play': play})

@login_required
def update_profile(request):
    user = request.user 

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("plays:profile")

    else:
        form = ProfileForm(instance=user)

    return render(request, "plays/profile.html", {"form": form, "user": user})
