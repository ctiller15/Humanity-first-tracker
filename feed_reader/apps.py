import os
from django.apps import AppConfig
from decouple import config
from feed_reader.scheduler_override import Scheduler

class FeedReaderConfig(AppConfig):
    name = 'feed_reader'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            from feed_reader.feed_job import job
            scheduler = Scheduler()
            scheduler.every(15).seconds.do(job)

            # do scheduler logic here.
            scheduler.run_continuously()
