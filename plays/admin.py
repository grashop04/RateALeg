from django.contrib import admin
from plays.models import Category
from plays.models import Play, Review, Feedback, CustomUser


admin.site.register(Category)
admin.site.register(Play)
admin.site.register(Review)
admin.site.register(Feedback)
admin.site.register(CustomUser)
