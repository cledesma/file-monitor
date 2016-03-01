#References 
#http://stackoverflow.com/questions/3987134/email-notification-on-file-change-in-particular-directory-with-python
#https://docs.python.org/2/library/email-examples.html

from file_monitor_service import FileMonitorService
import logging, logging.config
import os, time

logging.config.fileConfig('conf/logging.conf')

if __name__== "__main__":
    logging.info("start main")
    srv = FileMonitorService()
    while 1:
        srv.monitor_directory()
        time.sleep (10)
    logging.info("end main")


