import os, logging
import smtplib, ssl
import schedule, time
from datetime import datetime
from openWeatherMap_api_wrapper import get_fiveday_forcast

def run():
    sender_email = os.environ.get('sender_email')
    email_password = os.environ.get('email_password')
    openweather_api = os.environ.get('openweather_api')
    location = os.environ.get('location')
    receiver_email = os.environ.get('receiver_email')
    forcast_data = get_fiveday_forcast(location, openweather_api)
    newline = '\n \n'
    time_stamp = time.asctime(time.localtime(time.time()))
    message = f"""Subject: Test
    
    Good morning!
    Please see the following weather events over the next few days. \n Do we need to rebook the groundsmen jobs?:
    
    {newline.join(f'{key}: {value}' for key, value in forcast_data.items())}
    
    Kind regards,
    Weatherman
    """
    logging.basicConfig(filename='weather app.log', filemode='w')

    logging.info(f'[{time_stamp}]: Script successfully started!')

    def send_email(sender_email, receiver_email, message):
        context = ssl.create_default_context()
        port = 465

        with smtplib.SMTP_SSL('smtp.gmail.com',port, context=context) as server:
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, message)
        logging.info(f'[{time_stamp}]: Weather Warning sent!')
        return print(f'[{time_stamp}]: Weather alert sent')


    schedule.every().monday.at('07:00').do(send_email, sender_email, receiver_email, message)
    schedule.every().wednesday.at('07:00').do(send_email, sender_email, receiver_email, message)
    schedule.every().friday.at('07:00').do(send_email, sender_email, receiver_email, message)
    try:
        while True:
            if forcast_data != {}:
                schedule.run_pending()
                time.sleep(5)
            else:
                print('tick')
                time.sleep(60)
    except:
        logging.info(f'[{time_stamp}]: Script Ended!')

if __name__ == '__main__':
    run()