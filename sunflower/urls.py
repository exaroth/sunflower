from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from core.cbviews import (IndexView,
                          RedirectIndexView,
                          CreateAccountView,
                          AccountInfoView,
                          LoginScreenView,
                          ImageUploadView,
                          ImageDetailView,
                          ImageDeleteView,
                          JSONIndexImageView,
                          JSONAccountImageView,
                         )

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r"^$", IndexView.as_view(), name="index"),
                       url(r"^index/$", RedirectIndexView.as_view()),
                       url(r"^account_create/$", CreateAccountView.as_view(), name="account_create"),
                       url(r"^account/(?P<username>[0-9a-zA-Z_]{4,})$", AccountInfoView.as_view(), name="account_info"),
                       url(r"^login/$", LoginScreenView.as_view(), name='login'),
                       url(r"^logout/$", "core.views.logout_user", name="logout"),
                       url(r"^upload/$", ImageUploadView.as_view(), name="image_upload"),
                       url(r"image/(?P<pk>\d+)$", ImageDetailView.as_view(), name="image_detail"),
                       url(r"image/delete/(?P<pk>\d+)", ImageDeleteView.as_view(), name="image_delete"),
                       url(r"image_list/(?P<items>\d{1,2})/(?P<page>\d+)$", JSONIndexImageView.as_view(), name="image_json_view"),
                       url(r"user_image_list/(?P<pk>\d)", JSONAccountImageView.as_view(), name="account_image_json_view")
                      )
    

if settings.DEBUG:
    urlpatterns += patterns("",
                            url(r"^media/(?P<path>.*)$", "django.views.static.serve", {
                                "document_root": settings.MEDIA_ROOT,
                            })
                           )
