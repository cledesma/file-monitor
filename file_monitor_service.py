import os
import smtplib
import thread
import logging, logging.config

class FileMonitorService:

    def __init__(self):
        logging.config.fileConfig('conf/logging.conf')
        self.path_to_watch = "/tmp" #TODO Parameterize
        logging.info("Watching: " + self.path_to_watch)
        self.before = dict ([(f, None) for f in os.listdir (self.path_to_watch)])
        logging.info("Before: " + "\n".join(self.before))

    def monitor_directory(self):
        logging.info("*** begin monitor_directory ***")
        after = dict ([(f, None) for f in os.listdir (self.path_to_watch)])
        added = [f for f in after if not f in self.before]
        removed = [f for f in self.before if not f in after]
        if removed: logging.info("Removed: " + "\n".join(removed))
        if added:
            logging.info("Added: " + "\n".join(added))
            # thread.start_new_thread(self.run_ftp_mail_thread, ())
            thread.start_new_thread(self.run_ftp_mail_thread, ())
        self.before = after
        logging.info("*** end monitor_directory ***")

    def run_ftp_mail_thread(self):
        url = "http://www.ewise.com" #TODO
        self.send_mail(url)

    def send_mail(self,url):
        try: 
            logging.info("begin send_mail")
            email_username = os.environ['FILE_MONITOR_MAIL_USERNAME']
            email_password = os.environ['FILE_MONITOR_MAIL_PASSWORD']
            email_host = os.environ['FILE_MONITOR_MAIL_HOST']
            email_port = os.environ['FILE_MONITOR_MAIL_PORT']
            email_recipient = os.environ['FILE_MONITOR_MAIL_RECIPIENT']
            logging.info("mail username: " + email_username)
            logging.info("mail password: " + **************)
            logging.info("mail host: " + email_host)
            logging.info("mail.port: " + email_port)
            logging.info("mail recipient: " + email_recipient)
            to_list = []
            cc_list = []
            bcc_list = email_recipient
            header  = 'From: %s\n' % os.environ['FILE_MONITOR_MAIL_USERNAME']
            header += 'To: %s\n' % ','.join(to_list)
            header += 'Cc: %s\n' % ','.join(cc_list)
            header += 'Subject: %s\n\n' % "Client logs"
            message = header + url
            smtp_server = smtplib.SMTP(email_host, email_port)
            smtp_server.starttls()
            smtp_server.login(email_username, email_password)
            smtp_server.sendmail(email_username, bcc_list, message)
            smtp_server.quit()
            print "end send_mail"
        except Exception, e:
            logging.info("Exception: " + str(e))