import os
import smtplib
import thread
import logging, logging.config
import tinys3

class FileMonitorService:

    def __init__(self):
        logging.config.fileConfig('conf/logging.conf')
        self.path_to_watch = os.environ['FILE_MONITOR_PATH_TO_WATCH'] 
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
            for file in added:
                thread.start_new_thread(self.run_ftp_mail_thread, (file, self.path_to_watch,))
        self.before = after
        logging.info("*** end monitor_directory ***")

    def run_ftp_mail_thread(self, file, path_to_watch):
        logging.info("begin run_ftp_mail_thread")
        logging.info("file: " + file)
        logging.info("path_to_watch: " + path_to_watch)
        s3_access = os.environ['FILE_MONITOR_S3_ACCESS_KEY']
        s3_secret = os.environ['FILE_MONITOR_S3_SECRET_KEY']
        s3_bucket = os.environ['FILE_MONITOR_S3_BUCKET']
        s3_endpoint = os.environ['FILE_MONITOR_S3_ENDPOINT']
        logging.info("s3_bucket: " + s3_bucket)
        logging.info("s3_endpoint: " + s3_endpoint)
        conn = tinys3.Connection(s3_access,s3_secret,tls=True,endpoint=s3_endpoint)
        logging.info("path_to_watch + file: " + path_to_watch + file)
        f = open(path_to_watch + file,'rb')
        link = conn.upload(path_to_watch + file,f,s3_bucket)
        logging.info("S3 Link: " + str(link))

        url = "http://www.ewise.com" #TODO
        self.send_mail(url)
        logging.info("end run_ftp_mail_thread")

    def send_mail(self,url):
        try: 
            logging.info("begin send_mail")
            email_username = os.environ['FILE_MONITOR_MAIL_USERNAME']
            email_password = os.environ['FILE_MONITOR_MAIL_PASSWORD']
            email_host = os.environ['FILE_MONITOR_MAIL_HOST']
            email_port = os.environ['FILE_MONITOR_MAIL_PORT']
            email_recipient = os.environ['FILE_MONITOR_MAIL_RECIPIENT']
            logging.info("mail username: " + email_username)
            logging.info("mail password: **********l")
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