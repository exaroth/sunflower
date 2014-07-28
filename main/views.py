from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from main.models import Image
from main.forms import ImageUploadForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your views here.



def index(request):

    """
    Main index page showing all the images
    sorted by uploaded_date
    """

    context = dict()
    images = Image.objects.all()
    context["images"] = images

    return render(request, "index.html", context)


def upload(request):
    
    """
    Upload image views
    """

    context = dict()

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save(commit=False)
            # Refactor it later
            temp.thumb_path = "testing thumbs"
            user = User.objects.get()
            temp.uploader = user
            temp.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            print form.errors
            context["form"] = form
            return render(request, "upload.html", context )
    else:
        form = ImageUploadForm()
        context["form"] = form
        return render(request, "upload.html", context )
