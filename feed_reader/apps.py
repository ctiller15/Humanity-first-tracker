import os
from django.apps import AppConfig
from feed_reader.scheduler_override import Scheduler

class FeedReaderConfig(AppConfig):
    name = 'feed_reader'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            from feed_reader.feed_job import job
            scheduler = Scheduler()
            scheduler.every(15).minutes.do(job)

            scheduler.run_continuously()
