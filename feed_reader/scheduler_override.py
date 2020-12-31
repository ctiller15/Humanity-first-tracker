import logging
import time
import datetime
import threading
from schedule import Scheduler
from traceback import format_exc

logger = logging.getLogger('schedule')

class SchedulerOverride(Scheduler):
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

class SafeScheduler(SchedulerOverride):

    def __init__(self, reschedule_on_failure=True):
        self.reschedule_on_failure = reschedule_on_failure
        super().__init__()

    def _run_job(self, job):
        try:
            super()._run_job(job)
        except Exception:
            logger.error(format_exc())
            job.last_run = datetime.datetime.now()
            job._schedule_next_run()

    def run_continously(self, interval=1):
        try:
            super().run_continuously(interval)
        except Exception:
            logger.error(format_exc())
            job.last_run = datetime.datetime.now()
            job._schedule_next_run()
