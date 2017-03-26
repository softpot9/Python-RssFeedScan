import ConfigParser
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class SMTPEmailNotifier(object):
    '''
    This class is used to send a notifcation via SMTP email.
    '''

    smtp_user = None

    smtp_password = None

    smtp_server = None

    smtp_port = None

    notify_email = None

    smtp_tls = False


    def __init__(self, config_file):
        '''
        Constructor
        
        This configures the object from the config_file
        
        @param config_file: a path to the configuration file
        '''

        #Parse the configuration file
        config = ConfigParser.ConfigParser()

        config.readfp(open(config_file))

        self.smtp_user = config.get("Email Notifier", "smtpUser")

        self.smtp_password = config.get("Email Notifier", "smtpPassword")

        self.smtp_server = config.get("Email Notifier", "smtpServer")

        self.smtp_port = config.getint("Email Notifier", "smtpPort")

        self.notify_email = config.get("Email Notifier", "notifyEmail")

        self.smtp_tls = config.getboolean("Email Notifier", "smtpTLS")


    def notify(self, subject, message):
        '''
        Send an email message 
        
        @param message: The text message to be sent to the notified email.
        '''

        msg = MIMEMultipart()

        msg['subject'] = subject

        msg.attach(MIMEText(message, 'html'))

        mailServer = smtplib.SMTP(self.smtp_server, self.smtp_port, 5)

        mailServer.ehlo()

        try:

            if self.smtp_tls:
                mailServer.starttls()

            mailServer.ehlo()

            mailServer.login(self.smtp_user, self.smtp_password)

            mailServer.sendmail(self.smtp_user, self.notify_email, msg.as_string())

            mailServer.close()

        except Error as e:
            print "SMTP error({0}): {1}".format(e.errno, e.strerror)

        except:
            print "Failed to send email"

    def no_matches(self):
        '''
        Email notifications do not happen if no matches were found. Hence this
        is an empty method.
        '''
        
        return
