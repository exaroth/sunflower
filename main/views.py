from django.shortcuts import render
from django.http import HttpResponse
from main.models import Image

# Create your views here.



def index(request):

    context = dict()

    images = Image.objects.all()
    context["images"] = images

    return render(request, "index.html", context)

