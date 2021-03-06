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
    steps = 0

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [],
            'answers': []
        }

        # Количество пройденных им сообщений.

        res['response'][
            'text'] = 'Здравствуйте! Вам нужна помощь при выборе межвенцового утеплителя?\n\nВозможные варианты ответа: Да и Нет'
        # res['response']['buttons'] = get_suggests(user_id, ['Да', 'Нет'])
        return

    message = req['request']['original_utterance'].lower()

    # Обрабатываем ответ пользователя на нет.
    if message in [
        'нет',
        'не нужн',
        'не надо'
    ]:
        # Пользователь отказался, попытка номер 2
        res['response'][
            'text'] = 'Хорошо, в таком случае – я буду рядом и помогу Вам на этапах оформления покупки и доставки.\n\nЗдравствуйте! Вам нужна помощь при выборе межвенцового утеплителя?\n\nВозможные варианты ответа: Да и Нет'
        # res['response']['buttons'] = get_suggests(user_id, ['Да', 'Нет'])
        return

    # Обрабатываем ответ пользователя на да.
    elif message in [
        'да',
        'нужн',
        'необходим',
        'над'
    ]:
        res['response'][
            'text'] = f'Из какого материала Вы планируете строительство дома?\n\nВозможные варианты ответа: рубленное бревно, оцилиндрованное бревно, клееный брус, профилированный брус'
        steps = 1
        # res['response']['buttons'] = get_suggests(user_id, ['Рубленное бревно', 'Оцилиндрованное бревно', 'Клееный брус', 'Профилированный брус'])
        return

    # Обрабатываем ответ пользователя на последующие венцы.
    elif message in [
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
        # Пользователь согласился, узнаём что за материал.
        # Записываем его ответ для последующей обработки.
        add_answers(user_id, message)

        steps = 2
        # Пользователь согласился, узнаём для какого венца.
        res['response'][
            'text'] = 'Утеплитель необходим для первого венца, или – для последующих?\n\nВозможные варианты ответа: Для первого венца и Для последующих'
        # res['response']['buttons'] = get_suggests(user_id, ['Для первого венца', 'Для последующих венцов'])
        return

    elif message in [
        'для последующих венцов',
        'для последующих',
        'последующих',
        'последующий',
        'последующий венец'
    ]:
        # Пользователь согласился, узнаём для какого венца.
        # Записываем его ответ для последующей обработки.
        add_answers(user_id, 'последующий венец')
        mess(message, res, user_id)

    elif message in [
        'для первого венца',
        'для первого',
        'первый венец',
        'перв',
        'первого',
        'первый',
        '1'
    ]:
        # Пользователь согласился, узнаём для какого венца.
        # Записываем его ответ для последующей обработки.
        add_answers(user_id, 'первый венец')
        mess(message, res, user_id)
        # Обрабатываем ответ пользователя на последующие венцы.


# if steps == 4:
#     try:
#         # Обрабатываем ответ пользователя на числа.
#         shirina = int(float(req['request']['command']))
#         add_answers(user_id, str(shirina))
#         steps = 5
#         res['response']['text'] = 'Вот наиболее подходящие Вам варианты утеплителей. Выберите пожалуйста 1 вариант.'
#         return
#     except ValueError:
#         res['response'][
#             'text'] = 'Введите, пожалуйста, необходимую ширину ленты утеплителя. Эту информацию Вы можете найти в проекте дома в разделе «Спецификация материалов». Если этой информации нет проекте дома, или – проект дома у Вас отсутствует – уточните информацию у Ваших строителей. СТОП2'
#         return

# try:
#     if int(float(req['request']['original_utterance'])) == 15 or int(
#             float(req['request']['original_utterance'])) == 20:
#         # Обрабатываем ответ пользователя на числа.
#         vybor = int(float(req['request']['original_utterance']))
#         add_answers(user_id, vybor)
#         res['response'][
#             'text'] = f'1512Венец: {get_answers(user_id)[0]}, Материал: {get_answers(user_id)[1]}, Длина: {get_answers(user_id)[2]}, Ширина: {get_answers(user_id)[3]}'
#         return
# except ValueError:
#     res['response']['text'] = 'Выберите необходимую вам толщину утеплителя – 15 мм либо 20 мм.'
#     return
#
# try:
#     if int(float(req['request']['original_utterance'])) == 10 or int(
#             float(req['request']['original_utterance'])) == 20 or int(
#         float(req['request']['original_utterance'])) == 30:
#         # Обрабатываем ответ пользователя на числа.
#         vybor = int(float(req['request']['original_utterance']))
#         add_answers(user_id, vybor)
#         res['response'][
#             'text'] = f'102030 Венец: {get_answers(user_id)[0]}, Материал: {get_answers(user_id)[1]}, Длина: {get_answers(user_id)[2]}, Ширина: {get_answers(user_id)[3]}'
#         return
# except ValueError:
#     res['response']['text'] = 'Выберите необходимую вам толщину утеплителя – 5 мм либо 8 мм.'
#     return
#
# # # Если нет, то убеждаем его купить слона!
# # res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
# #     req['request']['original_utterance']
# # )
# # # res['response']['buttons'] = get_suggests(user_id)
# else:
# # Ошибка запроса.
# res['response']['text'] = 'Ошибка запроса.'
# return


def mess(message, res, user_id):
    # Если выбран клееный брус
    if get_answers(user_id)[0] in [
        'клееный брус',
        'клееный',
        'клеёный'
    ]:
        # Пользователь согласился, узнаём для какого венца.
        res['response']['text'] = 'Выберите необходимую вам толщину утеплителя – 5 мм либо 8 мм.'
        return

    elif get_answers(user_id)[0] in [
        'рубленное бревно',
        'рубленное',
        'рубленный',
        'рублённ'
    ]:
        # Пользователь согласился, узнаём для какого венца.
        res['response']['text'] = 'Выберите необходимую вам толщину утеплителя – 10 мм, 20 мм либо 30 мм.'
        return

    elif get_answers(user_id)[0] in [
        'оцилиндрованное бревно',
        'оцилиндрованное',
        'цилиндр',
        'профилированный брус',
        'профилированный',
        'профилированн'
    ]:
        # Пользователь согласился, узнаём для какого венца.
        res['response']['text'] = 'Выберите необходимую вам толщину утеплителя – 15 мм либо 20 мм.'
        return


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


# Добавляем ответы пользователей
def add_answers(user_id, answers):
    # Открываем сессию пользователя
    session = sessionStorage[user_id]

    # Добавляем ответы в массив
    session['answers'].append({answers})

    # Возвращаем ответы
    return session['answers']


# Получаем ответы пользователей
def get_answers(user_id):
    # Открываем сессию пользователя
    session = sessionStorage[user_id]

    # Из сессии получаем ответы
    answers = session['answers']

    # Возвращаем ответы
    return answers

# # Возвращает пройденные шаги пользователя
# def step(user_id):
#     session = sessionStorage[user_id]
#     return session['step']
#
#
# # Прибавливаем шаги пользователю
# def step(user_id, _int):
#     try:
#         session = sessionStorage[user_id]
#         session['step'] = _int
#         return session['step']
#     except BaseException:
#         return
#
#
# # Прибавливаем или вычитываем шаги пользователю.
# def step(user_id, _int, znak):
#     try:
#         if (znak != '-' and znak != '+'):
#             return
#         else:
#             session = sessionStorage[user_id]
#             if (znak == '-'):
#                 session['step'] -= _int
#             elif (znak == '+'):
#                 session['step'] += _int
#             return session['step']
#     except ValueError:
#         return
