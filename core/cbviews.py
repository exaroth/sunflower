from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import(
    TemplateView, ListView,
    RedirectView, DetailView,
    FormView
) 

from .models import Image, UserProfile
from .forms import UserCreateForm, UserProfileForm


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
    template_name = "account_create.html"
    success_url = "/"

    def get(self, request, *args, **kwargs):

        self.object = None
        form = UserCreateForm
        extended_form = UserProfileForm
        return self.render_to_response(self.get_context_data(form=form,
                                                             extended_form=extended_form))

    def post(self, request, *args, **kwargs):

        self.object = None
        form = UserCreateForm(request.POST)
        extended_form = UserProfileForm(request.POST, request.FILES)

        if(form.is_valid() and extended_form.is_valid()):
            print extended_form.cleaned_data
            return self.form_valid(form, extended_form)
        else:
            return self.form_invalid(form, extended_form)


    def form_valid(self, form, extended_form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = form.save(commit=True)
        user_profile = extended_form.save(commit=False)
        user_profile.user = user
        user_profile.save()

        return HttpResponseRedirect(reverse("index"))

    def form_invalid(self, form, extended_form):

        return self.render_to_response(self.get_context_data(
            form=form,
            extended_form = extended_form
        ))

class AccountInfoView(DetailView):

    model = User
    template_name = "account_info.html"
    context_object_name = "user_details"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):

        context = super(AccountInfoView, self).get_context_data(**kwargs)
        try:
            # Some users might not have additional info related to the
            # like admin
            additional = UserProfile.objects.get(user=self.get_object())
            context["additional_info"] = additional
        except Exception:
            pass
        return context


class LoginScreenView(FormView):

    form_class = AuthenticationForm
    template_name = "login_screen.html"

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
