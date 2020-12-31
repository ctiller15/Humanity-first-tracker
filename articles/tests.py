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

    def test_search_renders_within_date_range(self):
        category_names = ['ubi', 'andrew_yang', 'automation']
        articles = []
        start_date = '2020-12-28'
        end_date = '2020-12-30'

        valid_date = datetime(2020, 12, 29, tzinfo=pytz.utc)
        invalid_date = datetime(2020, 12, 15, tzinfo=pytz.utc)

        for category in category_names:
            new_category = create_category(category)
            new_article = create_article(new_category, valid_date)
            articles.append(new_article)

        invalid_articles = []
        for category in category_names:
            new_article = create_article(new_category, invalid_date)
            invalid_articles.append(new_article)

        response = self.client.get(f'/search_results?datefrom={start_date}&dateto={end_date}')
        response_str = str(response.content, 'utf-8')

        self.assertEqual(response.status_code, 200)
        for article in articles:
            self.assertIn(article.title, response_str)
            self.assertIn(article.link, response_str)

        for article in invalid_articles:
            self.assertNotIn(article.title, response_str)
            self.assertNotIn(article.link, response_str)

    def test_renders_all_past_articles_if_from_date_not_specified(self):
        category_names = ['ubi', 'andrew_yang', 'automation']
        articles = []
        end_date = '2020-12-30'

        valid_date = datetime(2020, 12, 29, tzinfo=pytz.utc)
        invalid_date = datetime(2020, 12, 15, tzinfo=pytz.utc)

        for category in category_names:
            new_category = create_category(category)
            new_article = create_article(new_category, valid_date)
            articles.append(new_article)

        old_articles = []
        for category in category_names:
            new_article = create_article(new_category, invalid_date)
            old_articles.append(new_article)

        response = self.client.get(f'/search_results?dateto={end_date}')
        response_str = str(response.content, 'utf-8')

        self.assertEqual(response.status_code, 200)
        for article in articles:
            self.assertIn(article.title, response_str)
            self.assertIn(article.link, response_str)

        for article in old_articles:
            self.assertIn(article.title, response_str)
            self.assertIn(article.link, response_str)

    def test_renders_all_future_articles_if_to_date_not_specified(self):
        category_names = ['ubi', 'andrew_yang', 'automation']
        categories = []
        articles = []
        start_date = '2020-12-28'
        end_date = '2020-12-30'

        future_date = datetime(2020, 12, 30, tzinfo=pytz.utc)
        valid_date = datetime(2020, 12, 29, tzinfo=pytz.utc)
        invalid_date = datetime(2020, 12, 15, tzinfo=pytz.utc)

        for category in category_names:
            new_category = create_category(category)
            categories.append(new_category)
            new_article = create_article(new_category, valid_date)
            articles.append(new_article)

        old_articles = []
        for category in categories:
            new_article = create_article(category, invalid_date)
            old_articles.append(new_article)

        future_articles = []
        for category in categories:
            new_article = create_article(category, future_date)
            future_articles.append(new_article)

        response = self.client.get(f'/search_results?datefrom={start_date}')
        response_str = str(response.content, 'utf-8')

        self.assertEqual(response.status_code, 200)
        for article in articles:
            self.assertIn(article.title, response_str)
            self.assertIn(article.link, response_str)

        for article in old_articles:
            self.assertNotIn(article.title, response_str)
            self.assertNotIn(article.link, response_str)

        for article in future_articles:
            self.assertIn(article.title, response_str)
            self.assertIn(article.link, response_str)

    def test_search_does_not_error_with_invalid_dates(self):
        category_names = ['ubi', 'andrew_yang', 'automation']
        articles = []
        start_date = 'gerwgerer43'
        end_date = 'g54gerfvsdgf43'

        valid_date = datetime(2020, 12, 29, tzinfo=pytz.utc)
        invalid_date = datetime(2020, 12, 15, tzinfo=pytz.utc)

        for category in category_names:
            new_category = create_category(category)
            new_article = create_article(new_category, valid_date)
            articles.append(new_article)

        invalid_articles = []
        for category in category_names:
            new_article = create_article(new_category, invalid_date)
            invalid_articles.append(new_article)

        response = self.client.get(f'/search_results?datefrom={start_date}&dateto={end_date}')
        response_str = str(response.content, 'utf-8')

        self.assertEqual(response.status_code, 200)
