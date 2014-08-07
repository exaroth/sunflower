from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import(
    TemplateView, ListView,
    RedirectView, DetailView
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
    template_name = "user_create.html"
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
        extended_form = UserProfileForm(request.POST)

        if(form.is_valid() and extended_form.is_valid()):
            print "form is valid"
            print form.cleaned_data
            return self.form_valid(form, extended_form)
        else:
            return self.form_invalid(form, extended_form)


    def form_valid(self, form, extended_form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        print username, password
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
    context_object_name = "account_user"
    slug_field = "username"
    slug_url_kwarg = "username"
