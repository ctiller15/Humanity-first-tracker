from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase, TestCase
from feed_reader.feed_job import clean_link, clean_bolds, job, get_site_url
from datetime import datetime
from uuid import uuid4
from feed_reader.models import Entry, Category

class TestFeedParser(SimpleTestCase):

    def test_title_cleaning(self):
        subtests = [
            ('<b>TEST</b>', 'TEST'),
            ('<b><b><b>String<b>', 'String')]

        for test_case, output in subtests:
            with self.subTest(test_case=test_case):
                self.assertEqual(output, clean_bolds(test_case))


    def test_site_extraction(self):
        subtests = [
            (
                'https://decrypt.co/52022/year-in-crypto-january-march',
                'decrypt.co'
            ),
            (
                'https://www.voanews.com/east-asia-pacific/taiwan-picked-favorite-superpower-2020-and-quashed-covid-19',
                'www.voanews.com'
            ),
            (
                'https://www.example.com',
                'www.example.com'
            ),
            (
                'https://www.newyorker.com/news/campaign-chronicles/how-the-democrats-are-turning-out-voters-in-georgia',
                'www.newyorker.com'
            )
        ]

        for test_case, output in subtests:
            with self.subTest(test_case=test_case):
                self.assertEqual(output, get_site_url(test_case))


    def test_link_cleaning(self):
        subtests = [(
            'https://www.google.com/url?rct=j&sa=t&url=https://decrypt.co/52022/year-in-crypto-january-march&ct=ga&cd=CAIyGmJlOWI3YmNlMDVlMGY2ZDE6Y29tOmVuOlVT&usg=AFQjCNE-YgWOyF-_199f00XT6KSzWEmiJw', 
            'https://decrypt.co/52022/year-in-crypto-january-march'
        ),
        (
            'https://www.google.com/url?rct=j&sa=t&url=https://www.voanews.com/east-asia-pacific/taiwan-picked-favorite-superpower-2020-and-quashed-covid-19&ct=ga&cd=CAIyGmJlOWI3YmNlMDVlMGY2ZDE6Y29tOmVuOlVT&usg=AFQjCNEW1NeUQPFokmbvUJNoGbcVHqqXqg',
            'https://www.voanews.com/east-asia-pacific/taiwan-picked-favorite-superpower-2020-and-quashed-covid-19'

        ),
        (
            'https://www.example.com',
            'https://www.example.com'
        )
                    ]

        for test_case, output in subtests:
            with self.subTest(test_case=test_case):
                self.assertEqual(output, clean_link(test_case))

class TestFeedParserJob(TestCase):
    mockDictionaryWithoutUpdatedDate = {
        'feed': {}
    }

    def mockFeedParser(data_url):
        unique_id = uuid4()
        test_date = datetime(2020, 12, 12, 20, 12, 30, 15)
        test_parsed_date = datetime(2020, 12, 12, 20, 12, 30, 15)

        mockDictionary = {
            'feed': {
                'updated_parsed': test_parsed_date.timetuple()
            },
            'entries': [
                {
                    'title': 'Really cool title here.',
                    'link': f'https://{unique_id}&https://www.example.com',
                    'summary': 'Entry summary!!!',
                    'published_parsed': test_parsed_date.timetuple(),
                    'updated_parsed': test_parsed_date.timetuple()
                }
            ]

        }

        return mockDictionary

    mockOpenGraphParseReturnWithoutTitles = {
        "og:image": 'fake image',
        "og:title": '',
        "og:site_name": 'https://fakesite.com'
    }

    @patch('feedparser.parse', mockFeedParser)
    @patch('opengraph_parse.parse_page', MagicMock(return_value={}))
    def test_job_reads_feeds_and_saves_data(self):
        self.assertEqual(len(Entry.objects.all()), 0)
        self.assertEqual(len(Category.objects.all()), 0)
        job()
        self.assertGreater(len(Entry.objects.all()), 0)
        self.assertGreater(len(Category.objects.all()), 0)

    @patch('feedparser.parse', mockFeedParser)
    @patch('opengraph_parse.parse_page', MagicMock(return_value=mockOpenGraphParseReturnWithoutTitles))
    def test_job_reads_feeds_and_saves_data_ignoring_empty_strings_for_og_parameters(self):
        self.assertEqual(len(Entry.objects.all()), 0)
        self.assertEqual(len(Category.objects.all()), 0)
        job()
        entries = Entry.objects.all()

        entry_site_names = [entry.og_site_name for entry in entries]
        entry_titles = [entry.og_title for entry in entries]
        entry_images = [entry.og_image for entry in entries]
    
        self.assertNotIn('', entry_site_names)
        self.assertNotIn('', entry_titles)
        self.assertNotIn('', entry_images)

    @patch('feedparser.parse', MagicMock(return_value=mockDictionaryWithoutUpdatedDate))
    @patch('opengraph_parse.parse_page', MagicMock(return_value=mockOpenGraphParseReturnWithoutTitles))
    def test_job_does_not_error_when_updated_date_empty(self):
        try:
            job()
        except  KeyError:
            self.fail('job() raised KeyError unexpectedly!')

