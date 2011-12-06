from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from articles.models import ArticleType, Article
from django.core.cache import cache

class RssSiteNewsFeed(Feed):
    title = "NeHe site news"
    link = "/"
    description = "News posts from http://nehe.gamedev.net/"

    def items(self):
        result = cache.get("RSS_NEWS_FEED")
        if result is None:            
            news_type = ArticleType.objects.get(description="NEWS")
            result = Article.objects.filter(published=True).filter(kind=news_type).order_by('-created_time')[:20]
            cache.set("RSS_NEWS_FEED", result, 60 * 60)
        return result

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.html_content
        
class AtomSiteNewsFeed(RssSiteNewsFeed):
    feed_type = Atom1Feed
    subtitle = RssSiteNewsFeed.description
