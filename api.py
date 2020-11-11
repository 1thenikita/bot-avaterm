# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging


from flask import Flask, render_template, request, make_response
from fuzzywuzzy import fuzz
from database import *
from random import randint


step = {}


class Bot:
    def __init__(self):
        step = {}
        self.answers = [
                            [
                                "Хорошо, в таком случае – я буду рядом и помогу Вам на этапах оформления покупки и доставки",
                                "Из какого материала Вы планируете строительство дома?"
                            ]
                       ]
        self.meta_data = {}

    def generate_answer(self, text, ip):
        if ip not in get_all_ip():
            if text.lower().strip() == "да":
                new_user(ip)
                return self.answers[0][1]
            elif text.lower().strip()  == "нет":
                return self.answers[0][0]
            else:
                return "Здравствуйте! Вам нужна помощь при выборе межвенцового утеплителя?"
        elif get_step(ip) == 1:
            if text.lower().strip() == "да":
                update_step(2, ip)
                return self.answers[0][1]
            elif text.lower().strip()  == "нет":
                return self.answers[0][0]
            else:
                return "Здравствуйте! Вам нужна помощь при выборе межвенцового утеплителя?"
        elif get_step(ip) == 2:
            if fuzz.ratio(text.lower().strip(), "рубленное бревно") >= 85:
                update_material("рубленное бревно", ip)
                update_step(3, ip)
                return "Утеплитель необходим для первого венца, или – для последующих?"
            elif fuzz.ratio(text.lower().strip(), "оцилиндрованное бревно") >= 85:
                update_material("оцилиндрованное бревно", ip)
                update_step(3, ip)
                return "Утеплитель необходим для первого венца, или – для последующих?"
            elif fuzz.ratio(text.lower().strip(), "клееный брус") >= 85:
                update_material("клееный брус", ip)
                update_step(3, ip)
                return "Утеплитель необходим для первого венца, или – для последующих?"
            elif fuzz.ratio(text.lower().strip(), "профилированный брус") >= 85:
                update_material("профилированный брус", ip)
                update_step(3, ip)
                return "Утеплитель необходим для первого венца, или – для последующих?"
            else:
                return self.answers[0][1]
            
        elif get_step(ip) == 3:
            if fuzz.ratio(text.strip().lower(), "для первого венца") >= 85:
                #self.meta_data[ip]["venec"] = 1
                update_step(4, ip)
                return "Введите, пожалуйста, общую длину ленты утеплителя в погонных метрах. Эту информацию Вы можете найти в проекте дома, в разделе «Спецификация материалов». Либо, если у вас его нет, можете самостоятельно рассчитать необходимое количество, сложив длину всех брёвен в домокомплекте."
            elif fuzz.ratio(text.strip().lower(), "для последующих") >= 85:
                #self.meta_data[ip]["venec"] = 2
                update_step(4, ip)
                return "Введите, пожалуйста, общую длину ленты утеплителя в погонных метрах. Эту информацию Вы можете найти в проекте дома, в разделе «Спецификация материалов». Либо, если у вас его нет, можете самостоятельно рассчитать необходимое количество, сложив длину всех брёвен в домокомплекте."
            else:
                return "Утеплитель необходим для первого венца, или – для последующих?"
        elif get_step(ip) == 4:
            try:
                #self.meta_data[ip]["dlina"] = int(text)
                update_step(5, ip)
                return "Выберите пожалуйста необходимую ширину ленты утеплителя. Эту информацию Вы можете найти в проекте дома в разделе «Спецификация материалов». Если этой информации нет проекте дома, или – проект дома у Вас отсутствует – уточните информацию у Ваших строителей."
            except:
                return "Введите целое число"
        elif get_step(ip) == 5:
            try:
                if 30 <= int(text) <= 350:
                    #self.meta_data[ip]["shirina"] = int(text)
                    update_step(6, ip)
                    if get_material(ip) == "рубленное бревно":
                        return "Вот наиболее подходящие Вам варианты утеплителей. Выберите пожалуйста 1 вариант.<br><br>Выберите необходимую вам толщину утеплителя – 10мм, 20мм либо 30мм."
                    elif get_material(ip) == "оцилиндрованное бревно":
                        return "Вот наиболее подходящие Вам варианты утеплителей. Выберите пожалуйста 1 вариант.<br><br>Выберите необходимую вам толщину утеплителя – 15мм либо 20мм."
                    elif get_material(ip) == "клееный брус":
                        return "Вот наиболее подходящие Вам варианты утеплителей. Выберите пожалуйста 1 вариант.<br><br>Выберите необходимую вам толщину утеплителя – 5мм либо 8мм."
                    elif get_material(ip) == "профилированный брус":
                        return "Вот наиболее подходящие Вам варианты утеплителей. Выберите пожалуйста 1 вариант.<br><br>Выберите необходимую вам толщину утеплителя – 15мм либо 20мм."
                else:
                    return "Введите целое число в диапазоне от 30 до 350"
            except:
                return "Введите целое число в диапазоне от 30 до 350"
        elif get_step(ip) == 6:
            if get_material(ip) == "рубленное бревно":
                try:
                    if int(text) in [10, 20, 30]:
                        update_step(1, ip)
                        return "Вот наиболее подходящие Вам варианты утеплителей. Выберите пожалуйста 1 вариант."
                    else:
                        return "Выберите необходимую вам толщину утеплителя – 10мм, 20мм либо 30мм."
                except:
                    return "Выберите необходимую вам толщину утеплителя – 10мм, 20мм либо 30мм."
            elif get_material(ip) == "оцилиндрованное бревно":
                try:
                    if int(text) in [15, 20]:
                        update_step(1, ip)
                        return "Вот наиболее подходящие Вам варианты утеплителей. Выберите пожалуйста 1 вариант."
                    else:
                        return "Выберите необходимую вам толщину утеплителя – 15мм либо 20мм."
                except:
                    return "Выберите необходимую вам толщину утеплителя – 15мм либо 20мм."
            elif get_material(ip) == "клееный брус":
                try:
                    if int(text) in [5, 8]:
                        update_step(1, ip)
                        return "Вот наиболее подходящие Вам варианты утеплителей. Выберите пожалуйста 1 вариант."
                    else:
                        return "Выберите необходимую вам толщину утеплителя – 5мм либо 8мм."
                except:
                    return "Выберите необходимую вам толщину утеплителя – 5мм либо 8мм."
            elif get_material(ip) == "профилированный брус":
                try:
                    if int(text) in [15, 20]:
                        update_step(1, ip)
                        return "Вот наиболее подходящие Вам варианты утеплителей. Выберите пожалуйста 1 вариант."
                    else:
                        return "Выберите необходимую вам толщину утеплителя – 15мм либо 20мм."
                except:
                    return "Выберите необходимую вам толщину утеплителя – 15мм либо 20мм."


app = Flask(__name__)

bots = Bot()

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


@app.route('/bot_question', methods=['POST'])
def bot():
    return bots.generate_answer(request.data.decode(), request.cookies.get('id_user'))


if __name__ == "__main__":
    app.run(threaded=True, port=5000)