import keyboard as kb
import json
import time
           

def start(url: str, key_start: str, key_exit: str, delay: float):
    while not kb.is_pressed(key_exit):
        if kb.is_pressed(key_start):
            kb.press_and_release("shift + enter")
            kb.write(url)
            kb.press_and_release("enter")
            time.sleep(delay)

def parse_msg(msg: str):
    parse_msg = msg.split(" ")
    parse_msg.remove(parse_msg[0])
    if len(parse_msg) == 0:
        print("Укажите имя профиля!")
        exit()
    else:
        return "_".join(map(str, parse_msg))

def main():
    while True:
        choice = input()
        if choice.startswith("default"):
            with open("./settings/settings.json", 'r') as file:
                args = json.load(file)
            args = args["profiles"]["default"]
            print(f"Активирован профиль default с параметрами {args}")
            start(str(args["url"]), args["key_start"], args["key_exit"], args["delay"])
        if choice.startswith("create-profile"):
            with open("./settings/settings.json", 'r') as file:
                profiles = json.load(file)
            profile_name = parse_msg(choice)
            print(f"Имя профиля: {profile_name}")
            if profile_name not in profiles["profiles"]:
                url = input("Введите ссылку на твич канал > ")
                key_start = input("Введите клавишу запуска > ")
                key_exit = input("Введите клавишу для выхода из программы > ")
                delay = float(input("Введите задержку отправки(в секундах) > "))
                profiles["profiles"][profile_name] = {
                    "url": url,
                    "key_start": key_start,
                    "key_exit": key_exit,
                    "delay": delay}
                with open("./settings/settings.json", 'w') as file:
                    json.dump(profiles, file, indent=4)
                args = profiles["profiles"][profile_name]
                print(f"Активирован профиль {profile_name} с параметрами {args}")
                start(str(args["url"]), args["key_start"], args["key_exit"], args["delay"])
            else:
                print("Профиль с таким именем уже существует!")
        if choice.startswith("use"):
            profile_name = parse_msg(choice)
            with open("settings.json", "r") as file:
                profiles = json.load(file)
            if profile_name not in profiles["profiles"]:
                print("Такого профиля не существует!")
            args = profiles["profiles"][profile_name]
            print(f"Активирован профиль {profile_name} с параметрами {args}")
            start(str(args["url"]), args["key_start"], args["key_exit"], args["delay"])
        if choice.startswith("profile-list"):
            with open("./settings/settings.json", 'r') as file:
                profiles = json.load(file)
            print(json.dumps(profiles, indent=2))
        else:
            print("Команда не найдена! Введите корректную команду")

if __name__ == '__main__':
    print("Команды:")
    print('''Использовать профиль по умолчанию (url - 1, f9 - start, f10 - exit, delay - 0s): default
Создать свой профиль: create-profile (profile_name)
Использовать уже существующий профиль: use (profile_name)
Посмотреть список профилей: profile-list''')
    main()