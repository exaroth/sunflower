from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, AddBorder, SmartResize
from imagekit import ImageSpec, register
from imagekit.utils import get_field_info
from south.modelsinspector import add_introspection_rules

add_introspection_rules([], [r"core.\thumb.\ImageSpecField"])

# Create your models here.

class ImageThumbnail(ImageSpec):

    format = "JPEG"
    options = {"quality": 80}
    cache_to="thumbnails"

    @property
    def processors(self):
        model, field = get_field_info(self.source)
        return [ResizeToFit(400)]

register.generator("core:image:image_thumbnail", ImageThumbnail)


class UserProfile(models.Model):


    user = models.OneToOneField(User, related_name="profile")
    homepage = models.URLField(blank=True)
    avatar = ProcessedImageField(upload_to="avatars",
                                 blank=True,
                                 processors=[SmartResize(100, 100)],
                                 format="JPEG",
                                 options={"quality": 80})

    def __unicode__(self):
        return self.user.username

class TimeStampMixin(models.Model):

    date_added = models.DateTimeField(auto_now=True, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Image(TimeStampMixin):

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, related_name="images")
    img = models.ImageField(upload_to="images")
    thumb = ImageSpecField(source="img",
                           id="core:image:image_thumbnail"
                          )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("image_details", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("date_added",)
        verbose_name = "Image"
        verbose_name_plural = "Images"

class Category(TimeStampMixin):

    name = models.CharField(max_length=40,
                            help_text="Category name",
                           )
    images = models.ManyToManyField(Image)


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


