from django.contrib import admin
from main.models import UserExt, Image

# Register your models here.

class UserExtAdmin(admin.ModelAdmin):
    
    
    class Meta:

        model = UserExt

class ImageAdmin(admin.ModelAdmin):

    class Meta:

        model = Image


admin.site.register(UserExt, UserExtAdmin)
admin.site.register(Image, ImageAdmin)

