from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponse, StreamingHttpResponse
from django.views.generic.list import BaseListView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core import serializers
from django.utils import simplejson
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic import(
    TemplateView, ListView,
    RedirectView, DetailView,
    FormView, DeleteView, CreateView,
    View
) 

from .models import Image, UserProfile
from .forms import (
    UserCreateForm, UserProfileForm,
    ImageAddForm, CategoryForm,
    CustomLoginForm
) 


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
    template_name = "auth/account_create.html"
    success_url = "/"

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("index"))

        self.object = None
        form = UserCreateForm
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = UserCreateForm(request.POST)
        if(form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = form.save(commit=True)
        
        authenticated = authenticate(username=username, password=password)
        login(self.request, authenticated)
        return HttpResponseRedirect(reverse("index"))

    def form_invalid(self, form):

        return self.render_to_response(self.get_context_data(
            form=form,
        ))

class AccountInfoView(DetailView):

    template_name = "auth/account_info.html"
    context_object_name = "user_details"
    slug_field = "username"
    slug_url_kwarg = "username"
    model = User
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.username != self.kwargs["username"]:
            raise Http404
        return super(AccountInfoView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(AccountInfoView, self).get_context_data(**kwargs)
        user_data = self.get_object()
        try:
            additional = user_data.profile
        except:
            additional = None
        images = user_data.images.all()
        context["additional_info"] = additional
        context["images"] = images
        return context

    def get_object(self):
        return self.model.objects.\
                filter(username=self.\
                       kwargs["username"]).select_related().get()


class LoginScreenView(FormView):

    form_class = CustomLoginForm
    template_name = "auth/login_screen.html"

    def form_valid(self, form):

        login(self.request, form.get_user())
        username = form.cleaned_data["username"]
        return HttpResponseRedirect(self.get_success_url(username))

    def get_success_url(self, username):
        return reverse_lazy("account_info", kwargs={"username": username})

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("index"))
        return super(LoginScreenView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ImageUploadView(CreateView):

    form_class = ImageAddForm
    category_form_class = CategoryForm
    template_name = "image_upload.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ImageUploadView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):

        new_image = form.save(commit=False)
        new_image.author = self.request.user
        new_image.save()
        return HttpResponseRedirect(reverse_lazy("image_detail", kwargs={"pk": new_image.pk}))

    def get(self, request, *args, **kwargs):

        self.object = None
        form = self.get_form(self.form_class)
        return self.render_to_response(self.get_context_data(
            form = form,
        ))

    def post(self, request, *args, **kwargs):

        self.object = None
        form = self.get_form(self.form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ImageDeleteView(DeleteView):

    model = Image
    template_name = "image_confirm_delete.html"


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ImageDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):

        return reverse_lazy("index")

    def get_object(self, queryset=None):

        obj = super(ImageDeleteView, self).get_object()
        print obj.author == self.request.user
        if obj.author != self.request.user:
            raise Http404()
        return obj


class ImageDetailView(DetailView):

    template_name = "image_detail.html"
    model = Image
    context_object_name = "image"

class JSONResponseView(object):
    
    """
    Implements basic methods for returning JSON response
    """

    def render_to_json_response(self, data, **context_kwargs):
        context_kwargs["content_type"] = "application/json"
        return StreamingHttpResponse(self.convert_to_json(data), **context_kwargs)

    def convert_to_json(self, data):
        return simplejson.dumps(data, indent=4)

class JSONImageView(JSONResponseView, View):
    
    model = Image
    max_items = 30
    json_fields = ("img", "title")

    def get(self, request, *args, **kwargs):
        return self.render_to_json_response(self.get_context_data())

    def get_pagination(self):
        limit = int(self.kwargs["items"])
        if limit > self.max_items:
            limit = self.max_items
        current_page = int(self.kwargs["page"])
        start = (current_page - 1)* limit
        end = current_page*limit
        return (start, end)

    def get_object(self):
        # Add logic for pagination here
        object_list = self.model.objects.all()
        return object_list

    def get_context_data(self):
        object_list = self.get_object()
        pagination = self.get_pagination()
        item_count = object_list.count()
        page = object_list[pagination[0]: pagination[1]].queryset_to_list()
        if not page:
            raise Http404()
        result = dict()
        result["_meta"] = dict(
             image_count = item_count,
             api_version = "0.0.1"

        )
        result["data"] = page
        return result
