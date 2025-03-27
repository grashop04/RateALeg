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
        {'username': 'sophie20', 'firstName': 'Sophie', 'secondName': '', 'bio': 'Psychology student who loves theatre',},
        {'username': 'dave45', 'firstName': 'Dave', 'secondName': '', 'bio': 'Passionate play critic'},
        {'username': 'rachel29', 'firstName': 'Rachel', 'secondName': '', 'bio': 'Actor starring in Dear Evan Hansen'},
    ]
    User = get_user_model()
    for user_info in users:
        user, created = User.objects.get_or_create(username=user_info['username'], defaults=user_info)

    plays_data = [
        {"title": "The Lion King", "WriterFirstName": "Roger", "WriterSecondName": "Allers", "genre": "Musical", "releaseDate": "2025-06-15", "description": "A young lion prince is cast out of his pride by his cruel uncle, who claims he killed his father. Based on the cult classic 1994 Disney movie. A must see with the family", "playImage": "images/lion_king.jpg", "location": "Kings Thetre", "spotify_code": "<iframe style='border-radius:12px' src='https://open.spotify.com/embed/album/3YA5DdB3wSz4pdfEXoMyRd?utm_source=generator' width='100%' height='352' frameBorder='0' allowfullscreen='' allow='autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture' loading='lazy'></iframe>"},
        {"title": "Annie, The Musical", "WriterFirstName": "Thomas", "WriterSecondName": "Meehan", "genre": "Musical", "releaseDate": "2025-04-21", "description": "A young orphan finds a new home with a billionaire. Based on the popular novel by Harold Gray, Annie has become a worldwide phenomenon and is the winner of 7 Tony Awards. Annie is the perfect family friendly musical and ideal show", "playImage": "images/annie.jpg", "location": "Tron Theatre", "spotify_code": "<p> help me </p>"},
        {"title": "The Phantom of the Opera", "WriterFirstName": "Andrew", "WriterSecondName": "Lloyd Webber", "genre": "Musical", "releaseDate": "1986-01-26", "description": "A disfigured musical genius, hidden away in the Paris Opera House, terrorizes the opera company. Based on the 1910 novel by Gaston Leroux. This musical is known for its elaborate sets, costumes and special effects, including the iconic chandelier crash.", "playImage": "images/phantom.jpg", "location": "Kings Theatre", "spotify_code": "help me"},
        {"title": "The Sound of Music", "WriterFirstName": "Richard", "WriterSecondName": "Rodgers", "genre": "Musical", "releaseDate": "2025-03-02", "description": "A nanny takes care of children and takes them on a magical adventure, based on the true story of the Von Trap family and their escape from Austria during the Nazi era, focusing on Maria, a governess and her impact on the familys musical life", "playImage": "images/sound_of_music.jpg", "location": "Tron Theatre", "spotify_code": "help me"},
        {"title": "The Book of Mormon", "WriterFirstName": "Trey", "WriterSecondName": "Parker", "genre": "Musical", "releaseDate": "2025-03-24", "description": "Two Mormon missionaries are sent to Uganda to try and convert the locals to Mormonism. The story is based on two young men who are challenged by the lack of interest in the locals, who are distracted more with the more pressing issue of HIV/AIDS", "playImage": "images/book_of_mormon.jpg", "location": "Theatre Royal Glasgow", "spotify_code": "help me"},  
        {"title": "Hamilton","WriterFirstName": "Lin-Manuel","WriterSecondName": "Miranda","genre": "Musical","releaseDate": "2015-01-20","description": "A revolutionary musical blending hip-hop, jazz, and R&B to tell the story of American Founding Father Alexander Hamilton. Winner of 11 Tony Awards, it redefines musical theatre with its diverse casting and groundbreaking score.","playImage": "images/hamilton.jpg","location": "SEC Armadillo", "spotify_code": "help me"},
        {"title": "Wicked","WriterFirstName": "Stephen","WriterSecondName": "Schwartz","genre": "Musical","releaseDate": "2003-10-30","description": "The untold story of the witches of Oz. Wicked follows Elphaba and Glinda before Dorothy dropped in, exploring friendship, power, and what makes a villain. Known for powerful ballads like 'Defying Gravity'.","playImage": "images/wicked.jpg","location": "Theatre Royal","spotify_code": "help me"},
        {"title": "Les Misérables","WriterFirstName": "Claude-Michel","WriterSecondName": "Schönberg","genre": "Musical","releaseDate": "1980-10-08","description": "Set in 19th-century France, Les Mis follows Jean Valjean, an ex-convict seeking redemption while pursued by Inspector Javert. An epic tale of revolution, justice and hope, with unforgettable songs like 'I Dreamed a Dream' and 'Do You Hear the People Sing?'.","playImage": "images/les_miserables.jpg","location": "King's Theatre", "spotify_code": "help me"},
        {"title": "Mamma Mia!","WriterFirstName": "Catherine","WriterSecondName": "Johnson","genre": "Musical","releaseDate": "1999-04-06","description": "A feel-good story told through ABBA's greatest hits. Set on a Greek island, a bride invites three men from her mother’s past in hopes of discovering her real father. A joyful journey of love, laughter, and disco.","playImage": "images/mamma_mia.jpg","location": "Pavilion Theatre", "spotify_code": "help me"},
        {"title": "Dear Evan Hansen","WriterFirstName": "Steven","WriterSecondName": "Levenson","genre": "Musical","releaseDate": "2015-07-10","description": "A powerful exploration of teenage anxiety, loneliness, and the desire to belong. Evan's life changes when a letter he wrote to himself is mistaken as a suicide note from a classmate. Touching and raw, it’s a voice for a generation.","playImage": "images/dear_evan_hansen.jpg","location": "Tron Theatre", "spotify_code" : "uh oh"}
    ]   

    for play_info in plays_data:
        naive_datetime = datetime.datetime.strptime(play_info["releaseDate"], "%Y-%m-%d")
        aware_datetime = make_aware(naive_datetime)

        play, created = Play.objects.get_or_create(title=play_info["title"])

     # Always update these fields in case they change
        play.WriterFirstName = play_info["WriterFirstName"]
        play.WriterSecondName = play_info["WriterSecondName"]
        play.genre = play_info["genre"]
        play.releaseDate = aware_datetime
        play.description = play_info["description"]
        play.playImage = play_info["playImage"]
        play.location = play_info["location"]
        play.date_play = aware_datetime
        play.spotify_code = play_info.get("spotify_code", "")


    play.save()

    print(f"{'Added' if created else 'Updated'} play: {play.title}")

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