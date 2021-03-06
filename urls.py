from django.conf.urls.defaults import *

from django.contrib import admin

admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

from public.rss import RssSiteNewsFeed, AtomSiteNewsFeed

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin/', include(admin.site.urls)),
    ('^$', 'public.views.homepage'),
    ('^tutorial/(.+?)/(?P<article_id>\d+)/$', 'public.views.view_article'),
    ('^article/(.+?)/(?P<article_id>\d+)/$', 'public.views.view_article'),
    ('^news/(.+?)/(?P<article_id>\d+)/$', 'public.views.view_article'),
    ('^listing/(.+?)/(?P<listing_id>\d+)/$', 'public.views.view_listing'),    
    ('^article_index/(?P<page>\d+)/', 'public.views.article_listing', { 'kind' : 'ARTICLE' }),
#    ('^_admin/$', 'articles.views.admin_home'),
#    ('^_admin/article/$', 'articles.views.admin_article_list'),
#    ('^_admin/article/add/$', 'articles.views.admin_article_create'),
#    ('^_admin/article/edit/(?P<article_id>\d+)/$', 'articles.views.admin_article_edit'),
#    ('^_admin/article_type/$', 'articles.views.admin_article_type_list'),
#    ('^_admin/article_type/add/$', 'articles.views.admin_article_type_create'),
#    ('^_admin/article_type/edit/(?P<article_type_id>\d+)/$', 'articles.views.admin_article_type_edit'),
#    ('^_admin/manage_cache/$', 'articles.views.admin_manage_cache'),
    ('^data/lessons/lesson.asp', 'public.views.legacy_tutorial_redirect'),
    ('^data/articles/article.asp', 'public.views.legacy_article_redirect'),
    ('^data/(?P<url>(.+?)\.(zip|jpg|png|gif|tar.gz|jar|7z))', 'public.views.legacy_data_redirect'),
    ('^lesson.asp', 'public.views.legacy_index_page_redirect'),
    (r'^rss/$', RssSiteNewsFeed()),
    (r'^atom/$', AtomSiteNewsFeed()),
)
