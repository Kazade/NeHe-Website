from datetime import datetime
from django.test import TestCase
from django.test import Client

from django.contrib.auth.models import User
from django.test.client import RequestFactory

from articles.globs import ArticleType
from articles.models import Article
from articles.models import ArticleType as ArticleTypeOld

from articles.tasks import update_article_types

from google.appengine.api.datastore import Get, Put
from utils import generate_cache_key, get_possible_url_cache_keys

class DataGenerator(object):
    def new_user(self, username, password="password"):
        u = User(username=username, email="test@example.com", password=password)
        u.save()
        return u        

    def new_news_post(self, title, body, author, published=True):       
        p = Article(article_type=ArticleType.NEWS, 
                    title=title,
                    html_content=body,
                    author=author,
                    published=published)
        p.save()                    
        return p

    def new_article_type(self, description, author=None):
        author = author or self.new_user("test" + datetime.strftime("%Y%m%d%s"))
        return ArticleTypeOld.objects.create(description=description, author=author)

    def new_article(self, title, body, author=None):
        author = author or self.new_user("test" + datetime.strftime("%Y%m%d%s"))    
        return Article.objects.create(title=title, html_content=body, article_type=ArticleType.ARTICLE, author=author)
    
class HomePageTest(TestCase, DataGenerator):
    def setUp(self):
        kazade = self.new_user("kazade")
        self.new_news_post("Test Post", "This is a test post", author=kazade)
    
    def test_works(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["news_posts"]["object_list"]), 1)
        
    def test_unpublished_dont_display(self):
        self.new_news_post("Other test", "Other", author=User.objects.get(), published=False)
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["news_posts"]["object_list"]), 1)        
        
    def test_converted_news_posts_display(self):
        post = self.new_news_post("Other test", "Other", author=User.objects.get())
        post.kind = ArticleTypeOld.objects.get(description="NEWS")
        post.article_type = None
        post.save()        
        
        update_article_types()
        
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["news_posts"]["object_list"]), 2)                       
        
class ArticleTypes(TestCase, DataGenerator):        
    def test_articles_by_kind(self):
        author = self.new_user("kazade")
    
        a1 = self.new_article("Test", "Test2", author=author)
        self.new_news_post("News", "News body", author=author)
        
        articles = Article.get_by_kind(ArticleType.ARTICLE)
        self.assertEqual(1, len(articles))
        self.assertEqual(articles[0], a1)        
        
class CacheKeyGeneratorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_cache_key_generation(self):
        req = self.factory.get("/")
        self.assertEqual("PAGE_HOME", generate_cache_key(req))
        
        req = self.factory.get("/?page=1")
        self.assertEqual("PAGE_HOME", generate_cache_key(req))
        
        req = self.factory.get("/?page=1")
        self.assertEqual("PAGE_HOME-[(page,1)]", generate_cache_key(req, ["page"]))                

        req = self.factory.get("/?page=1&elephant=2")
        self.assertEqual("PAGE_HOME-[(page,1)]", generate_cache_key(req, ["page"]))

        req = self.factory.get("/?page=1&elephant=2")
        self.assertEqual("PAGE_HOME-[(elephant,2),(page,1)]", generate_cache_key(req, ["page", "elephant"]))       
        
    def test_possible_cache_keys(self):
        result = get_possible_url_cache_keys("/", [ ("page", 1), ("page", 2) ])
        
        self.assertEqual(4, len(result))
        self.assertTrue("PAGE_HOME" in result)
        self.assertTrue("PAGE_HOME-[(page,1)]" in result)
        self.assertTrue("PAGE_HOME-[(page,2)]" in result)
        self.assertTrue("PAGE_HOME-[(page,1),(page,2)]" in result)
        
        result = get_possible_url_cache_keys("/mypage/something", [ ( "order_by", "id") ])
        self.assertEqual(2, len(result))
        self.assertTrue("PAGE_MYPAGE_SOMETHING" in result)
        self.assertTrue("PAGE_MYPAGE_SOMETHING-[(order_by,id)]" in result)        
        
        
