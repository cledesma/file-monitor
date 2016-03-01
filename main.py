#References 
#http://stackoverflow.com/questions/3987134/email-notification-on-file-change-in-particular-directory-with-python
#https://docs.python.org/2/library/email-examples.html

from file_monitor_service import FileMonitorService
from apscheduler.schedulers.background import BackgroundScheduler
import logging 
import os

logging.basicConfig(filename='file-monitor.log',level=logging.INFO)

if __name__== "__main__":

    logging.info("starting file-monitor")
    srv = FileMonitorService(logging)
    scheduler = BackgroundScheduler()
    logging.info("add job to scheduler")
    scheduler.add_job(srv.monitor_directory, 'interval', minutes=1)
    logging.info("begin scheduler")
    scheduler.start()

def loop_job(self, path_to_watch, before):
    logging.info("begin loop_job")
    before = srv.monitor_directory(path_to_watch, before)