import os, threading, json

PRESETS = os.getcwd() + "/presets"
OPERS = ["*", "/", "+", "-"]


class AliceResponse:
    def __init__(self, text, tts):
        self.text = text
        self.tts = tts
        self.data = {
            "response": {
                "text": self.text,
                "tts": self.tts,
                "buttons": [
                ],
                "end_session": False,
            },
            "session_state": {
            },
            "user_state_update": {
                "value": 0
            },

            "version": "1.0"
        }

    def add_button(self, title: str, url: str = None, payload: str = {}, hide: str = True):
        buttons = self.data["response"]["buttons"]
        buttons.append({"title": title, "url": url, "payload": payload, "hide": hide})

    def delete_button(self, title):
        buttons = self.data["response"]["buttons"]
        for i in range(len(buttons)):
            if buttons[i]["title"] == title:
                buttons.pop(i)
                return

    def set_session_state(self, value: tuple):
        self.data["session_state"].update({value[0]: value[1]})

    def get_session_state(self, key: str = None):
        return self.data["session_state"] if key is None else self.data["session_state"]["key"]

    def json(self):
        return self.data


class User:
    def __init__(self, preset=["+", "-"]):
        self.__preset = preset

    def preset(self):
        return self.__preset

    def set_preset(self, preset: list):
        self.__preset += preset


connection = {}


def find_file(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
            return True
    return False


def create_preset(*args):
    json_data = {
        "presets": args[1],
        "count": [0, 0],
        "education": {}
    }
    with open(f"{PRESETS}/{args[0]}.json", "w") as f:
        json.dump(json_data, f)


def first_message():
    resp = AliceResponse("Здравствуйте, вы в навыке пошёл нафиг!", "Д+а")
    resp.add_button("Практика", payload={"command": "practice"})
    resp.add_button("Обучение", payload={"command": "education"})
    resp.add_button("Сколько решено?", payload={"command": "count"})
    resp.set_session_state(("branch", "main",))
    resp.set_session_state(("command", "",))
    return resp.json()


def main(command, session_state, request, user=None):
    resp = None
    match command:
        case "first_message":
            return first_message()

        case "practice":
            text = """Вы попали в практику! \n
                                    1.Конструктор примеров - 
                                    понятие \n
                                    2.Назвать возраст - подобрать рекомендованный список 
                                    задач \n
                                    """
            resp = AliceResponse(text, "В+ы перешл+и в пр+актику!")
            if find_file(f"{user}.json", PRESETS):
                resp.add_button("Продолжить с прошлыми настройками", payload={"command": "agreed"})
                resp.set_session_state(("branch", "practice"))
                resp.set_session_state(("command", "practice"))
            resp.add_button("Конструктор примеров", payload={"command": "construct"})
            resp.add_button("Ваш возраст?", payload={"command": "ages"})
            resp.set_session_state(("branch", "main",))
            resp.set_session_state(("command", "practice",))

        case "education":
            pass

        case "count":
            find_file(f"{user}.json", PRESETS)
            with open(f"{PRESETS}/{user}.json") as f:
                data = json.load(f)
            count_all = data["count"][0]
            count_success = data["count"][1]
            resp = AliceResponse(f"Сегодня вы решали {count_all}. {count_success} правильно!",
                                 f"Сег+одня вы реш+али {count_all}. {count_success} пр+авильно!")
            resp.set_session_state(("command", "first_message"))
            resp.add_button("Практика", payload={"command": "practice"})
            resp.add_button("Обучение", payload={"command": "education"})
            resp.add_button("Сколько решено?", payload={"command": "count"})
            resp.set_session_state(("branch", "main",))
            resp.set_session_state(("command", "",))

        case "construct":
            resp = AliceResponse("Ты можешь выбрать операторы, тебе нужно называть их в 1 сообщении",
                                 "Ты можешь выбрать операторы, тебе нужно называть их в 1 сообщении")
            resp.set_session_state(("branch", "main"))
            resp.set_session_state(("command", "construct_agree",))
            connection[user] = connection.get(str(user), User())

        case "construct_agree":
            connection[user].set_preset([x for x in list(request["original_utterance"]) if x in OPERS])
            preset = connection[user].preset()

            resp = AliceResponse(f"Знаки которые ты выбрал: {', '.join(preset)}",
                                 f"Знаки которые ты выбрал: {', '.join(preset)}")
            resp.add_button("Всё верно!", payload={"command": "agreed"})
            resp.add_button("Отменить", payload={"command": "first_message"})
            resp.add_button("Добавить", payload={"command": "construct"})
            resp.set_session_state(("branch", "main"))
            resp.set_session_state(("command", "agreed"))
        case "agreed":
            if connection.get(user, False):
                th = threading.Thread(target=create_preset, args=(user, connection[user].preset()))
                th.start()
            resp = AliceResponse(f"Вы попали в практику!", "Да")
            resp.add_button("Начать!", payload={"command": "start"})
            resp.set_session_state(("branch", "practice"))
            resp.set_session_state(("command", "start"))
        case _:
            resp = AliceResponse("Выбери одно из предложенных!", "В+ыбери одн+о из предл+оженных!")
            resp.add_button("Практика", payload={"command": "practice"})
            resp.add_button("Обучение", payload={"command": "education"})
            resp.add_button("Сколько решено?", payload={"command": "count"})
            resp.set_session_state(("branch", "main",))
            resp.set_session_state(("command", "",))

    return resp.json()
