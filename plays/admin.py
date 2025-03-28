from django.contrib import admin
from plays.models import Category, Play, Review, Feedback, CustomUser

# Admin configuration for Rate A Leg application

# Register Category model - used for play classifications
admin.site.register(Category)

# Register Play model - main entity representing theatrical plays
admin.site.register(Play)

# Register Review model - user-submitted ratings and comments
admin.site.register(Review)

# Register Feedback model - user feedback about the platform
admin.site.register(Feedback)

# Register CustomUser model - extended user model for authentication
admin.site.register(CustomUser)