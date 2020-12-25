from django.apps import AppConfig
import os
import schedule
from schedule import Scheduler
import time
import threading

def job():
    print("Doing the thing!")

def run_continuously(self, interval=1):

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously

class FeedReaderConfig(AppConfig):
    name = 'feed_reader'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            scheduler = Scheduler()
            scheduler.every(10).seconds.do(job)

            # do scheduler logic here.
            print("Check me out!")
            scheduler.run_continuously()
