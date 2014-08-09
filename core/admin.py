from django.contrib import admin
from imagekit.admin import AdminThumbnail

from .models import Image, UserProfile



class ImageAdmin(admin.ModelAdmin):

    list_display = ("__str__", "author")

class UserProfileAdmin(admin.ModelAdmin):
    
    def profile_username(self, instance):

        return instance.user.username

    list_display = ("__str__", "homepage")

admin.site.register(Image, ImageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

