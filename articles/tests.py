from django.test import TestCase
from django.urls import reverse
from feed_reader.models import Category, Entry
from uuid import uuid4
from datetime import datetime, timedelta
import pytz

def create_category(name):
    category = Category.objects.create(name=name)
    category.save()
    return category

def create_article(category, date=None):
    today_date = date if date else datetime.now().replace(tzinfo=pytz.UTC)
    unique_identifier = uuid4()
    title = f'title{unique_identifier}'
    link = f'link{unique_identifier}'
    link_dirty = f'link_dirty{unique_identifier}'
    new_entry = Entry.objects.create(title=title, link=link, link_dirty=link_dirty, category=category, published=today_date, updated=today_date)
    new_entry.save()
    return new_entry 

# Split into unit tests and integration tests
class TestArticles(TestCase):

    def test_home_page(self):
        category_names = ['ubi', 'andrew_yang', 'automation']
        articles = []
        for category in category_names:
            new_category = create_category(category)
            new_article = create_article(new_category)
            articles.append(new_article)

        url = '/'
        response = self.client.get(url)
        response_str = str(response.content, 'utf-8')

        self.assertEqual(response.status_code, 200)
        for article in articles:
            self.assertIn(article.title, str(response.content, 'utf-8'))
            self.assertIn(article.link, response_str)

    def test_home_page_renders_even_if_no_data(self):
        url = '/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)

    def test_home_page_renders_last_thirty_days_of_results_by_default(self):
        category_names = ['ubi', 'andrew_yang', 'automation']
        articles = []
        for category in category_names:
            new_category = create_category(category)
            new_article = create_article(new_category)
            articles.append(new_article)

        old_date = datetime.now(pytz.UTC) - timedelta(30)
        old_articles = []
        for category in category_names:
            new_article = create_article(new_category, old_date)
            old_articles.append(new_article)

        response = self.client.get('/')
        response_str = str(response.content, 'utf-8')

        self.assertEqual(response.status_code, 200)
        for article in articles:
            self.assertIn(article.title, response_str)
            self.assertIn(article.link, response_str)

        for article in old_articles:
            self.assertNotIn(article.title, response_str)
            self.assertNotIn(article.link, response_str)
