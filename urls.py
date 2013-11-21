from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'application.views.index'),
    url(r'^account/', include('registration.backends.default.urls')),
    url(r'^account/login_redirect', 'application.views.login_redirect'),
    url(r'^user/(?P<user_name>\w{1,50})/$', 'application.views.user_view'),
    url(r'^story/index/$', 'application.views.story_index'),
    url(r'^story/index/admin$', 'application.views.story_index_admin'),
    url(r'^story/new/$', 'application.views.story_new'),
    url(r'^story/(?P<story_id>\d+)/$', 'application.views.story_view'),
    url(r'^story/randomise/(?P<story_id>\d+)/$', 'application.views.story_randomise'),
    url(r'^story/edit/(?P<story_id>\d+)/$', 'application.views.story_edit'),
    url(r'^story/save/$', 'application.views.story_save'),
    url(r'^story/delete/$', 'application.views.story_delete'),
    url(r'^upload/$', 'application.views.upload'),
    url(r'^help/$', 'application.views.help'),
    url(r'^about/$', 'application.views.about'),
    url(r'^analysis/$', 'application.views.analysis'),



    url(r'^logger/$', 'application.views.logger'),
    url(r'^admin/', include(admin.site.urls)),
)
