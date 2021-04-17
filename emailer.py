import smtplib, ssl, time, logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, receiver_email, email_password, subject, message_body):
    logging.basicConfig(filename='weather app.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S',
                        level=logging.DEBUG)
    logging.info('Sending email...')
    try:
        message_template = MIMEMultipart()
        message_template['Subject'] = subject
        message_template['From'] = sender_email
        message_template['To'] = receiver_email
        text = message_body
        message_part = MIMEText(text, 'plain')
        message_template.attach(message_part)
        time_stamp = time.asctime(time.localtime(time.time()))
        context = ssl.create_default_context()
        port = 465
        with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, message_template.as_string())
        logging.info('Email successfully sent!')
        return print(f'[{time_stamp}]: Email sent.')
    except:

        logging.error('There was an error sending an email.')
        return print('error with sending email')