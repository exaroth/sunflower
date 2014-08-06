from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from core.cbviews import IndexView

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'sunflower.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r"^$", IndexView.as_view(), name="index"),
                      )

if settings.DEBUG:
    urlpatterns += patterns("",
                            url(r"^media/(?P<path>.*)$", "django.views.static.serve", {
                                "document_root": settings.MEDIA_ROOT,
                            })
                           )
