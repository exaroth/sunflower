from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse

# Create your views here.

def logout_user(request):

    logout(request)
    return HttpResponseRedirect(reverse("index"))
