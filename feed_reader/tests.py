from django.test import SimpleTestCase
from feed_reader.feed_job import clean_link, clean_bolds

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

        )
                    ]

        for test_case, output in subtests:
            with self.subTest(test_case=test_case):
                self.assertEqual(output, clean_link(test_case))
