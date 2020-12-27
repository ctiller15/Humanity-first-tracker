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
        category_name = 'fake category'
        new_category = create_category(category_name)
        new_article = create_article(new_category)

        url = '/'
        response = self.client.get(url)
        response_str = str(response.content, 'utf-8')

        self.assertEqual(response.status_code, 200)
        self.assertIn(new_article.title, str(response.content, 'utf-8'))
        self.assertIn(new_article.link, response_str)
