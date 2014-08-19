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
from django.views.decorators.cache import cache_page, never_cache
from django.core.cache import get_cache
from django.conf import settings
from django.core import serializers
from django.utils import simplejson
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import FormMixin
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
    CustomLoginForm, ImageDescriptionForm
) 

cache = get_cache("default")


class IndexView(TemplateView):

    paginate_by = 10
    context_object_name = "images"
    template_name="index.html"
    
    # @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class RedirectIndexView(RedirectView):

    url = "/"


class CreateAccountView(CreateView):

    model = User
    form_class = UserCreateForm
    template_name = "auth/account_create.html"
    success_url = "/"

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(CreateAccountView, self).dispatch(*args, **kwargs)

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
        user_profile = UserProfile(user=user)
        user_profile.save()
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
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        if self.request.user.username != self.kwargs["username"]:
            raise Http404

        return super(AccountInfoView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = None
        if request.user.is_superuser:
            return HttpResponseRedirect("/admin")
        additional_info_form = UserProfileForm(instance=self.get_object().profile)
        return self.render_to_response(self.get_context_data(additional_info_form))
        
    def post(self, request, *args, **kwargs):
        self.object = None
        if request.user.is_superuser:
            return HttpResponseRedirect("/admin")
        additional_info_form = UserProfileForm(request.POST, request.FILES, instance = self.get_object().profile)
        if additional_info_form.is_valid():
            return self.form_valid(additional_info_form)
        return self.form_invalid(additional_info_form)

    def form_valid(self, form):
        
        new_profile_data = form.save(commit=False)
        new_profile_data.user = self.request.user
        new_profile_data.save()
        return HttpResponseRedirect(reverse_lazy("account_info", kwargs={"username": self.request.user.username }))

    def form_invalid(self, form):

        return self.render_to_response(self.get_context_data(form))


    def get_context_data(self, additional_info, **kwargs):
        context = super(AccountInfoView, self).get_context_data(**kwargs)
        user_data = self.get_object()
        images = user_data.images.all()
        context["additional_info"] = additional_info
        context["images"] = images
        return context

    def get_object(self):
        return self.request.user


class LoginScreenView(FormView):

    form_class = CustomLoginForm
    template_name = "auth/login_screen.html"
    
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginScreenView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):

        login(self.request, form.get_user())
        username = form.cleaned_data["username"]
        return HttpResponseRedirect(self.get_success_url(username))

    def get_success_url(self, username):
        next = self.request.GET.get("next", None)
        if not next:
            next = reverse_lazy("account_info", kwargs={"username": username})
        return next

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
        cache.clear()
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

        return reverse_lazy("account_info", kwargs={"username": self.request.user.username})

    def get_object(self, queryset=None):

        obj = super(ImageDeleteView, self).get_object()
        if obj.author != self.request.user:
            raise Http404()
        return obj


class ImageDetailView(DetailView, FormMixin):

    template_name = "image_detail.html"
    model = Image
    context_object_name = "image"
    form_class = ImageDescriptionForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        img = self.get_object()
        if img.author != self.request.user:
            return HttpResponseForbidden()
        return super(ImageDetailView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ImageDetailView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context["form"] = self.get_form(form_class)
        return context


    def get_form_kwargs(self):
        kwargs = super(ImageDetailView, self).get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        cache.clear()
        return HttpResponseRedirect(reverse_lazy("image_detail", kwargs = {"pk": self.get_object().pk}))


class JSONResponseView(object):
    
    """
    Implements basic methods for returning JSON response
    """

    def dispatch(self, *args, **kwargs):
        if not self.request.is_ajax() and not settings.DEBUG:
            raise Http404
        return super(JSONResponseView, self).dispatch(*args, **kwargs)

    def render_to_json_response(self, data, **context_kwargs):
        context_kwargs["content_type"] = "application/json"
        return StreamingHttpResponse(self.convert_to_json(data), **context_kwargs)

    def convert_to_json(self, data):
        return simplejson.dumps(data, indent=4)


class JSONIndexImageView(JSONResponseView, View):
    
    model = Image
    max_items = 30

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
        pagination = self.get_pagination()
        object_list = self.get_object()
        item_count = object_list.count()
        cache_name = "index_image_item_{0}".format(self.kwargs["page"])
        index_page = cache.get(cache_name)
        if index_page:
            page = index_page
        else:
            page = object_list[pagination[0]: pagination[1]].queryset_to_list()
            cache.set(cache_name, page, 4 * 60)
        if not page:
            raise Http404()
        result = dict()
        result["_meta"] = dict(
             image_count = item_count,
             api_version = "0.0.1"

        )
        result["data"] = page
        return result

class JSONAccountImageView(JSONResponseView, View):

    model = User
    json_fields = ("thumb", "pk")

    def get(self, *args, **kwargs):
        return self.render_to_json_response(self.get_context_data())

    def get_object(self):

        try:
            user = self.model.objects.get(pk=self.kwargs["pk"])
        except:
            raise Http404
        cached_data_name = "account_images_{0}".format(self.kwargs["pk"])
        cached_images = cache.get(cached_data_name)
        if cached_images:
            object_list = cached_images
            print object_list
        else:
            object_list = user.images.all()
            print object_list
            cache.set(cached_data_name, object_list, 3 * 60)
        return object_list

    def get_context_data(self):
        
        result = dict()
        object_list = self.get_object().queryset_to_list(self.json_fields)
        result["data"] = object_list

        return result
