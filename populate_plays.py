import os
import django
import datetime
from django.utils.timezone import make_aware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rate_a_leg_project.settings')
django.setup()

from plays.models import Play, Category, CustomUser, Review
from django.contrib.auth import get_user_model 

def populate():

    categories = ['Musical', 'Drama', 'Comedy']
    for category in categories:
        Category.objects.get_or_create(name=category)

    users = [
        {'username': 'sophie20', 'firstName': 'Sophie', 'secondName': '', 'bio': 'Psychology student who loves theatre'},
        {'username': 'dave45', 'firstName': 'Dave', 'secondName': '', 'bio': 'Passionate play critic'},
        {'username': 'rachel29', 'firstName': 'Rachel', 'secondName': '', 'bio': 'Actor starring in Dear Evan Hansen'},
    ]
    User = get_user_model()
    for user_info in users:
        user, created = User.objects.get_or_create(username=user_info['username'], defaults=user_info)

    plays_data = [
        {"title": "The Lion King", "WriterFirstName": "Roger", "WriterSecondName": "Allers", "genre": "Musical", "releaseDate": "2025-06-15", "description": "A young lion prince is cast out of his pride by his cruel uncle, who claims he killed his father.", "playImage": "images/lion_king.jpg"},
        {"title": "Annie, The Musical", "WriterFirstName": "Thomas", "WriterSecondName": "Meehan", "genre": "Musical", "releaseDate": "2025-04-21", "description": "A young orphan finds a new home with a billionaire.", "playImage": "images/annie.jpg"},
        {"title": "The Phantom of the Opera", "WriterFirstName": "Andrew", "WriterSecondName": "Lloyd Webber", "genre": "Musical", "releaseDate": "1986-01-26", "description": "A disfigured musical genius, hidden away in the Paris Opera House, terrorizes the opera company", "playImage": "images/phantom.jpg"},
        {"title": "The Sound of Music", "WriterFirstName": "Richard", "WriterSecondName": "Rodgers", "genre": "Musical", "releaseDate": "2025-03-02", "description": "A nanny takes care of children and takes them on a magical adventure.", "playImage": "images/sound_of_music.jpg"},
        {"title": "The Book of Mormon", "WriterFirstName": "Trey", "WriterSecondName": "Parker", "genre": "Musical", "releaseDate": "2025-03-24", "description": "Two Mormon missionaries are sent to Uganda to try and convert the locals to Mormonism.", "playImage": "images/book_of_mormon.jpg"},  
    ]

    for play_info in plays_data:
        naive_datetime = datetime.datetime.strptime(play_info["releaseDate"], "%Y-%m-%d")
        aware_datetime = make_aware(naive_datetime)
        play, created = Play.objects.get_or_create(
            title=play_info["title"],
            defaults={
                "WriterFirstName": play_info["WriterFirstName"],
                "WriterSecondName": play_info["WriterSecondName"],
                "genre": play_info["genre"],
                "releaseDate": aware_datetime,
                "description": play_info["description"],
                "playImage": play_info["playImage"],
            }
        )
        if created:
            print(f"Added new play: {play.title}")
        else:
            print(f"Play already exists: {play.title}")

    reviews = [
    {
        "username": "sophie20",
        "play_title": "The Lion King",
        "SoundTrackRating": 4,
        "CastRating": 5,
        "SetRating": 3,
        "AverageRating": 4,
        "comment": "Sample review"
    },
    {
        "username": "dave45",
        "play_title": "Annie, The Musical",
        "SoundTrackRating": 5,
        "CastRating": 5,
        "SetRating": 5,
        "AverageRating": 5,
        "comment": "Sample review"
    },
    {
        "username": "rachel29",
        "play_title": "The Lion King",
        "SoundTrackRating": 3,
        "CastRating": 4,
        "SetRating": 5,
        "AverageRating": 4,
        "comment": "Sample review"
    },
]

    for review_info in reviews:
        user = User.objects.get(username=review_info["username"])
        play = Play.objects.get(title=review_info["play_title"])
        review, created = Review.objects.get_or_create(
            username=user, 
            playId=play,
            SoundTrackRating=review_info["SoundTrackRating"],
            CastRating=review_info["CastRating"],
            SetRating=review_info["SetRating"],
            AverageRating=review_info["AverageRating"],
            comment=review_info["comment"],
        )

   

if __name__ == '__main__':
    print('Starting play population script...')
    populate()