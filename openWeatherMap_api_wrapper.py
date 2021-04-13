import requests
import logging
import time
from datetime import datetime
import os


def get_fiveday_forcast(city_name, api_key):
    # Modify the individual ranges to alter the severity of the weather type added to the dictionary. See link below:
    # Weather id list: https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
    weather_id_list = [
        [201, 202, 231, 232],
        [301, 302, 311, 312, 313, 314, 321],
        [500, 501, 502, 503, 504, 511, 521, 522, 531],
        [601, 602, 611, 613, 616, 621, 622]
    ]
    weather_dict = {}
    # https://openweathermap.org/forecast5#parameter
    path = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}'
    session = requests.session()
    try:
        response = session.get(path)
        json_data = response.json()
        # Break down Json to get date, time, and weather condition
        for weather_items in json_data['list']:
            weather_id = int(weather_items['weather'][0]['id'])
            weather_type = weather_items['weather'][0]['description']
            weather_datetime = str(datetime.strptime(weather_items['dt_txt'],
                                                     '%Y-%m-%d %H:%M:%S')).split(' ')
            weather_dow = datetime.strptime(weather_datetime[0], '%Y-%m-%d')
            weather_dow = weather_dow.strftime('%A')
            for weather_id_range in weather_id_list:
                if weather_id in weather_id_range:
                    if weather_dow != ['Saturday', 'Sunday']:
                        weather_dict.setdefault(weather_datetime[0], {'Time of Day': weather_datetime[1],
                                                 'Weather Type': weather_type})
    except Exception:
        logging.basicConfig(filename='weather app.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%d-%m-%Y %H:%M:%S',
                            level=logging.DEBUG)
        logging.exception(f'An error has occurred\n---------------------------------------------------')
    return weather_dict
