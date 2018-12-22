import requests
import datetime


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]
        return last_update


def get_weather(app_id, location):
        try:
            res = requests.get(" http://api.openweathermap.org/data/2.5/weather?q={0}&APPID={1}"
                               .format(location, app_id))
            data = res.json()
            return "Conditions: {}\nTemperature: {}"\
                .format(data['weather'][0]['description'], data['main']['temp'] - 273.15)
        except Exception as e:
            pass
            # print("Exception (weather):", e)


def greet():
    new_offset = None
    month, today, hour = now.month, now.day, now.hour

    greet_bot.get_updates(new_offset)
    last_update = greet_bot.get_last_update()

    last_update_id = last_update['update_id']
    last_chat_text = last_update['message']['text']
    last_chat_id = last_update['message']['chat']['id']
    last_chat_name = last_update['message']['chat']['first_name']

    if today == now.day and 6 <= hour < 12:
        greet_bot.send_message(last_chat_id, 'Доброе утро,  {}'.format(last_chat_name))
        today += 1
    elif today == now.day and 12 <= hour < 17:
        greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
        today += 1
    elif today == now.day and 17 <= hour < 23:
        greet_bot.send_message(last_chat_id, 'Добрый вечер,  {}'.format(last_chat_name))
        today += 1
    greet_bot.send_message(last_chat_id, 'Где посмотреть погоду (odessa,ua)?')
    new_offset = last_update_id + 1
    while True:
        greet_bot.get_updates(new_offset)
        last_update = greet_bot.get_last_update()
        last_update_id = last_update['update_id']
        if last_update_id == new_offset:
                get_location()
                new_offset = last_update_id+1


def get_location():
    app_id = 'b3ca393ab7255938ea9a02c469408cbb'
    greet_bot.get_updates(None)
    last_update = greet_bot.get_last_update()

    last_chat_text = last_update['message']['text']
    last_chat_id = last_update['message']['chat']['id']
    weather_info = get_weather(app_id, last_chat_text)
    greet_bot.send_message(last_chat_id, weather_info)


if __name__ == '__main__':
    greet_bot = BotHandler('792677523:AAHCAsRplF1zxwEBShZBWPClLi5sl5X6k9I')
    now = datetime.datetime.now()

    try:
        greet()
        # get_location()
    except KeyboardInterrupt:
        exit()
