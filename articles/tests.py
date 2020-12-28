from django.test import TestCase
from django.urls import reverse
from feed_reader.models import Category, Entry
from uuid import uuid4
from datetime import datetime

def create_category(name):
    category = Category.objects.create(name=name)
    category.save()
    return category

def create_article(category):
    unique_identifier = uuid4()
    title = f'title{unique_identifier}'
    link = f'link{unique_identifier}'
    link_dirty = f'link_dirty{unique_identifier}'
    new_entry = Entry.objects.create(title=title, link=link, link_dirty=link_dirty, category=category, published=datetime.now(), updated=datetime.now())
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
