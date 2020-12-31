import os
from django.apps import AppConfig
from feed_reader.scheduler_override import SafeScheduler

class FeedReaderConfig(AppConfig):
    name = 'feed_reader'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            from feed_reader.feed_job import job
            scheduler = SafeScheduler()
            scheduler.every(15).seconds.do(job)

            scheduler.run_continuously()
