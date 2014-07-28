from django.contrib import admin
from main.models import UserExt, Image

# Register your models here.

class UserExtAdmin(admin.ModelAdmin):

    def user_name(self, instance):

        return instance.user.username

    list_display = ("user_name",)

    

class ImageAdmin(admin.ModelAdmin):

    def user_name(self, instance):

        return instance.uploader.username

    list_display = ("title", "uploader", "modified")

admin.site.register(UserExt, UserExtAdmin)
admin.site.register(Image, ImageAdmin)

