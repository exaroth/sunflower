from django.contrib import admin

from .models import Image, UserProfile



class ImageAdmin(admin.ModelAdmin):

    list_display = ("title", "author")

class UserProfileAdmin(admin.ModelAdmin):
    
    def profile_username(self, instance):

        return instance.user.username

    list_display = ("homepage", "profile_username")

admin.site.register(Image, ImageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

