import os
import requests
import telegram
import time
import logging
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# URL_PRACTIKUM = os.getenv('URL_PRACTIKUM') не пропускает сервер на проверку
# URL_REQUEST = os.getenv('URL_REQUEST') не пропускает сервер на проверку
URL_PRACTIKUM = 'https://praktikum.yandex.ru/api/user_api/'
URL_REQUEST = 'homework_statuses/'

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    status = homework.get('status')
    if not (homework_name and status):
        logging.error('Произошла ошибка при запросе')
        return f'Не найдено домашнее задание, проверьте запрос.'
    if status not in ['rejected', 'approved']:
        logging.error('Произошла ошибка при запросе')
        verdict = f'Неизвестный статус домашнего задания {homework_name}'
    if status == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    if status == 'approved':
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    if current_timestamp is None or isinstance(current_timestamp, int):
        current_timestamp = int(time.time())
    try:
        homework_statuses = requests.get(f"{URL_PRACTIKUM}{URL_REQUEST}", headers=headers, params=params)
        return homework_statuses.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = int(time.time())

    while True:
        print(get_homework_statuses(current_timestamp))
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]))
            current_timestamp = new_homework.get('current_date')  # обновить timestamp
            time.sleep(300)  # опрашивать раз в пять минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
