from datetime import datetime
from django.test import TestCase
from django.test import Client

from django.contrib.auth.models import User

from articles.globs import ArticleType
from articles.models import Article
from articles.models import ArticleType as ArticleTypeOld

from articles.tasks import update_article_types

from google.appengine.api.datastore import Get, Put

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
        
        