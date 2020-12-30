from unittest.mock import patch
from django.test import SimpleTestCase, TestCase
from feed_reader.feed_job import clean_link, clean_bolds, job
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
    def mockFeedParser(data_url):
        unique_id = uuid4()
        test_date = datetime(2020, 12, 12, 20, 12, 30, 15)
        test_parsed_date = datetime(2020, 12, 12, 20, 12, 30, 15)

        mockDictionary = {
            'feed': {
                'updated_parsed': {
                    'tm_year': test_date.year,
                    'tm_mon': test_date.month,
                    'tm_mday': test_date.day,
                    'tm_hour': test_date.hour,
                    'tm_min': test_date.minute,
                    'tm_sec': test_date.second,
                },
            },
            'entries': [
                {
                    'title': 'Really cool title here.',
                    'link': f'{unique_id}&https://www.example.com',
                    'summary': 'Entry summary!!!',
                    'published_parsed': {
                        'tm_year': test_parsed_date.year,
                        'tm_mon': test_parsed_date.month,
                        'tm_mday': test_parsed_date.day,
                        'tm_hour': test_parsed_date.hour,
                        'tm_min': test_parsed_date.minute,
                        'tm_sec': test_parsed_date.second,
                    },
                    'updated_parsed': {
                        'tm_year': test_parsed_date.year,
                        'tm_mon': test_parsed_date.month,
                        'tm_mday': test_parsed_date.day,
                        'tm_hour': test_parsed_date.hour,
                        'tm_min': test_parsed_date.minute,
                        'tm_sec': test_parsed_date.second,
                    }
                }
            ]

        }

        return mockDictionary

    @patch('feedparser.parse', mockFeedParser)
    def test_job_reads_feeds_and_saves_data(self):
        self.assertEqual(len(Entry.objects.all()), 0)
        self.assertEqual(len(Category.objects.all()), 0)
        job()
        self.assertGreater(len(Entry.objects.all()), 0)
        self.assertGreater(len(Category.objects.all()), 0)
