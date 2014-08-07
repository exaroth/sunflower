from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import forms
from django.http import Http404
from django.views.generic import(
    TemplateView, ListView,
    RedirectView, DetailView
) 

from .models import Image
from .forms import UserCreateForm


class IndexView(ListView):

    queryset = Image.objects.all()
    paginate_by = 10
    context_object_name = "images"
    template_name="index.html"

    def get_context_data(self):

        context = super(IndexView, self).get_context_data()
        
        return context

class RedirectIndexView(RedirectView):

    url = "/"


class CreateAccountView(CreateView):

    model = User
    form_class = UserCreateForm
    template_name = "user_create.html"
    success_url = "/"


class AccountInfoView(DetailView):

    model = User
    template_name = "account_info.html"
    context_object_name = "account_user"
    slug_field = "username"
    slug_url_kwarg = "username"
