# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [],
            # 'suggets2': [
            #     "Рублённое бревно",
            #     "Оцилиндрованное бревно",
            #     "Клееный брус",
            #     "Профилированный брус",
            # ]
            # 'suggets3': [
            #     "Для первого венца",
            #     "Для последующих",
            # ]
            'answers': []
        }

        res['response']['text'] = 'Здравствуйте! Вам нужна помощь при выборе межвенцового утеплителя?'
        res['response']['buttons'] = get_suggests(user_id, ['Да', 'Нет'])
        return

    # Обрабатываем ответ пользователя на нет.
    if req['request']['original_utterance'].lower() in [
        'нет'
    ]:
        # Пользователь отказался, попытка номер 2
        res['response']['text'] = 'Здравствуйте! Вам нужна помощь при выборе межвенцового утеплителя?'
        res['response']['buttons'] = get_suggests(user_id, ['Да', 'Нет'])
        return

    # Обрабатываем ответ пользователя на да.
    if req['request']['original_utterance'].lower() in [
        'да'
    ]:
        # Пользователь согласился, узнаём для какого венца.
        res['response']['text'] = 'Утеплитель необходим для первого венца, или – для последующих?'
        res['response']['buttons'] = get_suggests(user_id, ['Для первого венца', 'Для последующих венцов'])
        return

    # Обрабатываем ответ пользователя на первые венцы.
    if req['request']['original_utterance'].lower() in [
        'для первого венца',
        'для первого',
        'первый венец'
    ]:
        # Пользователь согласился, узнаём для какого венца.

        # Записываем его ответ для последующей обработки.
        add_answers(user_id, 'первый венец')

        res['response']['text'] = 'Из какого материала Вы планируете строительство дома?'
        res['response']['buttons'] = get_suggests(user_id, ['Рубленное бревно', 'Оцилиндрованное бревно', 'Клееный брус', 'Профилированный брус'])
        return
    
    # Обрабатываем ответ пользователя на последующие венцы.
    if req['request']['original_utterance'].lower() in [
        'для последующих венцов',
        'для последующих',
        'последующих',
        'последующий',
        'последующий венец'
    ]:
        # Пользователь согласился, узнаём для какого венца.
        # Записываем его ответ для последующей обработки.
        add_answers(user_id, 'последующий венец')

        res['response']['text'] = 'Из какого материала Вы планируете строительство дома?'
        res['response']['buttons'] = get_suggests(user_id, ['Рубленное бревно', 'Оцилиндрованное бревно', 'Клееный брус', 'Профилированный брус'])
        return

    # Обрабатываем ответ пользователя на последующие венцы.
    if req['request']['original_utterance'].lower() in [
        'рубленное бревно',
        'оцилиндрованное бревно',
        'клееный брус',
        'профилированный брус',
        'рубленное',
        'рубленный',
        'оцилиндрованное',
        'клееный',
        'профилированный'
    ]:
        # Пользователь согласился, узнаём для какого венца.
        # Записываем его ответ для последующей обработки.
        add_answers(user_id, req['request']['original_utterance'].lower())

        res['response']['text'] = 'Введите число в диапазоне от 30 до 350 мм.'
        return
    
    try:
        # Обрабатываем ответ пользователя на последующие венцы.
        if int(req['request']['original_utterance']):
            res['response']['text'] = 'Вы ввели число, лол.'
            return
    except ValueError:
        res['response']['text'] = 'Введите число в диапазоне от 30 до 350 мм.'


    # # Если нет, то убеждаем его купить слона!
    # res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
    #     req['request']['original_utterance']
    # )
    # res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает подсказки для ответа.
def get_suggests(user_id, _suggest):
    # Открываем сессию пользователя
    session = sessionStorage[user_id]

    # Обнуляем массив с подсказками.
    suggests = []

    # Через цикл добавляем подсказки в массив
    for i in range(len(_suggest)):
        suggests.append({
            "title": _suggest[i],
            "hide": True
        })

    # Возвращаем подсказки
    return suggests

# Функция возвращает подсказки для перехода по ссылке.
def get_url_suggests(user_id, _suggest):
    # Открываем сессию пользователя
    session = sessionStorage[user_id]

    # Обнуляем массив с подсказками.
    suggests = session['suggests'] = []

    # Через цикл добавляем подсказки в массив
    for i in range(len(_suggest)):
        suggests.append({
            "title": _suggest[i][0],
            "url": _suggest[i][1],
            "hide": True
        })

    # Возвращаем подсказки
    return suggests

def add_answers(user_id, answers):
    # Открываем сессию пользователя
    session = sessionStorage[user_id]

    # Из сессии получаем ответы
    answers = session['answers']

    # Через цикл добавляем ответы в массив
    for i in range(len(answers)):
        answers.append({answers[i]})

    # Возвращаем ответы
    return answers

def get_answers(user_id, answers):
    # Открываем сессию пользователя
    session = sessionStorage[user_id]

    # Из сессии получаем ответы
    answers = session['answers']

    # Возвращаем ответы
    return answers