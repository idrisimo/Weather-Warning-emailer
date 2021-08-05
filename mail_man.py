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
    time_stamp = time.asctime(time.localtime(time.time()))
    print(f'[{time_stamp}]: Script successfully started!')
    logging.info(f'Script successfully started!')

    admin_email = os.environ.get('admin_email')
    sender_email = os.environ.get('sender_email')
    email_password = os.environ.get('email_password')
    openweather_api = os.environ.get('openweather_api')
    location = os.environ.get('location')
    receiver_email = os.environ.get('receiver_email')
    forcast_data = get_fiveday_forcast(location, openweather_api)
    newline = '\n\n'
    subject = 'Weather Report'
    if forcast_data:
        print(f'[{time_stamp}]: Adverse Weather detected...')
        logging.info('Adverse Weather detected.')
        message = f"""Good morning!\n
        Please see the following weather events over the next few days.\n 
        Do we need to rebook the groundsmen jobs?\n
        {newline.join(f'{key}: {value}' for key, value in forcast_data.items())}\n
        Weatherman"""
    else:
        print(f'[{time_stamp}]: No Adverse Weather detected...')
        logging.info('No Adverse Weather detected.')
        message = f"""Good morning!\n
                No adverse weather detected for the next few days!\n 
                Hopefully its nothing but sunshine and rainbows!\n
                Weatherman"""


    schedule.every().monday.at('06:00').do(send_email, sender_email, receiver_email, email_password, subject, message)
    schedule.every().tuesday.at('06:00').do(send_email, sender_email, receiver_email, email_password, subject, message)
    schedule.every().wednesday.at('06:00').do(send_email, sender_email, receiver_email, email_password, subject, message)
    schedule.every().thursday.at('06:00').do(send_email, sender_email, receiver_email, email_password, subject, message)
    schedule.every().friday.at('06:00').do(send_email, sender_email, receiver_email, email_password, subject, message)
    schedule.every().sunday.at('06:00').do(send_email, sender_email, receiver_email, email_password, subject, message)

    try:
        print(f'[{time_stamp}]: Main loop starting!')
        logging.info(f'Main loop starting!')
        while True:
            schedule_counter = schedule.idle_seconds()
            if schedule_counter is None:
                print(f'[{time_stamp}]: No jobs left')
                logging.info(f'No jobs left.')
            elif schedule_counter > 0:
                print(f'[{time_stamp}]: Waiting for scheduled email slot...\n {schedule_counter} second(s) until next slot')
                logging.info(f'Waiting for scheduled email slot.')
                time.sleep(schedule_counter)
            schedule.run_pending()




    except Exception:
        logging.info(f'Script Ended in ISSUE!')
        send_email(sender_email, admin_email, email_password, 'Weather Watcher Issue', 'Issue with weather watcher. Script ended')
        print(f'[{time_stamp}]: Script Ended!')

    logging.info(f'Script Ended!')
if __name__ == '__main__':
    run()
