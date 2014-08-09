from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):


    user = models.OneToOneField(User)
    homepage = models.URLField(blank=True)
    portrait = models.ImageField(upload_to="portraits", blank=True)


    def __unicode__(self):
        return self.user.username

class TimeStampMixin(models.Model):

    date_added = models.DateTimeField(auto_now=True, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Image(TimeStampMixin):

    title = models.CharField(max_length=120)
    author = models.ForeignKey(User)
    path = models.ImageField(upload_to="images")
    thumb_path = models.ImageField(upload_to="thumbnails", blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ("date_added",)
        verbose_name = "Image"
        verbose_name_plural = "Images"

class Category(TimeStampMixin):

    name = models.CharField(max_length=40,
                            help_text="Category name",
                           choices=[("depro", "fundis")])
    images = models.ManyToManyField(Image)


    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


