from django.contrib import admin
from main.models import UserExt

# Register your models here.

class UserExtAdmin(admin.ModelAdmin):
    
    
    class Meta:

        model = UserExt


admin.site.register(UserExt, UserExtAdmin)

