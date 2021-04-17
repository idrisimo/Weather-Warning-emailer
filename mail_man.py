import os
import logging
import schedule
import time
from openWeatherMap_api_wrapper import get_fiveday_forcast
from dotenv import load_dotenv
from emailer import send_email


load_dotenv()

def run():
    logging.basicConfig(filename='weather app.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S',
                        level=logging.DEBUG)
    admin_email = os.environ.get('admin_email')
    sender_email = os.environ.get('sender_email')
    email_password = os.environ.get('email_password')
    openweather_api = os.environ.get('openweather_api')
    location = os.environ.get('location')
    receiver_email = os.environ.get('receiver_email')
    forcast_data = get_fiveday_forcast(location, openweather_api)
    newline = '\n'
    time_stamp = time.asctime(time.localtime(time.time()))
    subject = 'Weather Report'
    message = f"""Good morning!\n
    Please see the following weather events over the next few days.\n 
    Do we need to rebook the groundsmen jobs?:\n
    {newline.join(f'{key}: {value}' for key, value in forcast_data.items())}\n
    Weatherman"""
    print(f'[{time_stamp}]: Script successfully started!')
    logging.info(f'Script successfully started!')

    schedule.every().monday.at('05:00').do(send_email, sender_email, receiver_email, email_password, subject, message)
    schedule.every().wednesday.at('05:00').do(send_email, sender_email, receiver_email, email_password, subject, message)
    schedule.every().friday.at('05:00').do(send_email, sender_email, receiver_email, email_password, subject, message)

    '''schedule.every(1).minute.do(send_email, sender_email, receiver_email, email_password, subject, message)'''
    try:
        while True:
            if forcast_data != {}:
                print(f'[{time_stamp}]Adverse weather detected. Waiting for scheduled slot...')
                schedule.run_pending()
                time.sleep(5)
            else:
                print(f'[{time_stamp}]:tick')
                time.sleep(60)
    except:
        logging.info(f'Script Ended in ISSUE!')
        send_email(sender_email, admin_email, email_password, 'Weather Watcher Issue', 'Issue with weather watcher. Script ended')
        print(f'[{time_stamp}]: Script Ended!')

    logging.info(f'Script Ended!')
if __name__ == '__main__':
    run()
