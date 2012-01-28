import logging
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from djangotoolbox.fields import ListField
from google.appengine.api import memcache
from django.conf import settings
import string

from articles.globs import ARTICLE_TYPE_CHOICES
from articles.globs import ArticleType as ArticleTypeEnum

from public.utils import get_possible_url_cache_keys

class ArticleType(models.Model):
    description = models.CharField(max_length=255, unique=True)

    class Meta(object):
        app_label = "articles"    

    def __unicode__(self):
        return self.description

class MenuBlock(models.Model):
    name = models.CharField(max_length=64)
    active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    
    class Meta(object):
        app_label = "articles"
        
    def __unicode__(self):
        return self.name

    def get_menu_groups(self):
        return self.groups.filter(active=True).order_by('active', '-priority').all()

class MenuGroup(models.Model):
    block = models.ForeignKey(MenuBlock, related_name="groups")
    name = models.CharField(max_length=64, unique=True)
    priority = models.IntegerField()
    active = models.BooleanField(default=False)
    
    class Meta(object):
        app_label = "articles"
        
    def __unicode__(self):
        return self.name
    
    def get_articles(self):
        return self.articles.filter(published=True).order_by('published','created_time').all()
    
    def get_links(self):
        return self.links.order_by('text').all()

class Link(models.Model):
    menu_group = models.ForeignKey(MenuGroup, related_name="links")
    text = models.CharField(max_length=255)
    url = models.CharField(max_length=1024)
    
    is_important = models.BooleanField(default=False)
    
    class Meta(object):
        app_label = "articles"
        
    def __unicode__(self):
        if self.is_important:
            return '<strong><a href="%s">%s</a></strong>' % (self.url, self.text)    
        return '<a href="%s">%s</a>' % (self.url, self.text)

class FileUpload(models.Model):
    uploaded_file = models.FileField(upload_to='/upload')
    
class ArticleListing(models.Model):
    title = models.CharField(max_length=255)
    articles = ListField(models.PositiveIntegerField(), default=[], null=False)
    
    def __unicode__(self):
        return self.title
        
    class Meta(object):
        app_label = "articles"
        
    def get_absolute_url(self):
        return "/listing/%s/%i/" % (self.url_name(), self.pk)
        
    def url_name(self):
        s = self.title.lower()
        exclude = set(string.punctuation)
        s = ''.join(ch for ch in s if ch not in exclude)
        return s.replace(" ", "_") 
    
class Article(models.Model):
    kind = models.ForeignKey(ArticleType, null=True)
    article_type = models.CharField(max_length=32, choices=ARTICLE_TYPE_CHOICES, default=ARTICLE_TYPE_CHOICES[0][0], blank=False)
    author = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=512)
    html_content = models.TextField()
    
    published = models.BooleanField(default=False)
    menu_group = models.ForeignKey(MenuGroup, null=True, blank=True, related_name="articles")
    
    original_id = models.IntegerField(null=True, blank=True, default=None)
    sort_id = models.IntegerField(default=0)
    
    comments_enabled = models.BooleanField(default=False)
        
    tooltip_html = models.TextField(null=True, blank=True)
        
    def __unicode__(self):
        return self.title
    
    class Meta(object):
        app_label = "articles"
    
    def get_absolute_url(self):
        return "/%s/%s/%i/" % (self.article_type.lower(),
                               self.url_name(),
                               self.pk)

    def url_name(self):
        s = self.title.lower()
        exclude = set(string.punctuation)
        s = ''.join(ch for ch in s if ch not in exclude)
        return s.replace(" ", "_")

    def save(self, *args, **kwargs):
        #Always enable comments for news articles
        if self.article_type == ArticleTypeEnum.NEWS:
            self.comments_enabled = True
        else:
            self.comments_enabled = False

        result = super(Article, self).save(*args, **kwargs)

        #Delete the homepage and article cache keys
        cache_keys = []
        if self.published and (self.menu_group or self.article_type == ArticleTypeEnum.NEWS):
            cache_keys.extend(get_possible_url_cache_keys("/", [("page", 1), ("page",2)]))
        cache_keys.extend(get_possible_url_cache_keys(self.get_absolute_url()))

        for key in cache_keys:
            logging.info("Clearing cache key: %s" % key)
            cache.delete(key)
        return result
        
    def get_summary(self):
        return self.html_content.split('<!-- break -->')[0]
    
    @staticmethod
    def get_by_kind(description):
        return Article.objects.filter(article_type=description)
    
    @staticmethod
    def cache_or_get(kind, limit=None, group=None):
        key = "ARTICLE_CACHE_%s" % type.upper()        
        if limit:
            key += "_%i" % limit
        
        if group:
            key += "_GROUP_%i" % group.pk
        
        articles = memcache.get(key)
        
        if settings.DEBUG: 
            articles = None
            
        if not articles:        
            articles = Article.objects.filter(published=True).filter(article_type=kind).order_by('-created_time')
            if group:
                articles = articles.filter(group=group)
                
            if limit:
                articles = articles[:limit]
                
            memcache.add(key, articles, 60)
            
        return articles
        
class UserProfile(models.Model):
    adsense_code = models.CharField(max_length=255, null=False, blank=True, default='')
    adsense_slot = models.CharField(max_length=255, null=False, blank=True, default='')
    leaderboard_adsense_code = models.CharField(max_length=255, null=False, blank=True, default='')
    leaderboard_adsense_slot = models.CharField(max_length=255, null=False, blank=True, default='')
    flattr_user_id = models.CharField(max_length=255, null=False, blank=True, default='')
    
    license_under_cc = models.BooleanField(default=False)
    homepage_url = models.CharField(max_length=1024, null=True, blank=True)
    
    user = models.ForeignKey(User, unique=True)
    
    class Meta(object):
        app_label = "articles"
        
    def __unicode__(self):
        return self.user.username + u"'s profile"
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

    
