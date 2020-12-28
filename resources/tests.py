from django.test import TestCase
from resources.models import Resource
from uuid import uuid4

def createDummyResource():
    unique_id = uuid4()

    new_resource = Resource.objects.create(
        title=f'title{unique_id}',
        summary=f'summary{unique_id}',
        link=f'link{unique_id}',
        order=1,
        hidden=False
    )

    return new_resource

class TestResources(TestCase):

    def test_resources_page_renders_resource(self):
        resource = createDummyResource()
        
        url = '/resources/'
        response = self.client.get(url)
        response_str = str(response.content, 'utf-8')

        self.assertEqual(response.status_code, 200)

        self.assertIn(resource.title, response_str)
        self.assertIn(resource.summary, response_str)
        self.assertIn(resource.link, response_str)


