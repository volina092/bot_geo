import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import random
import json
import pymorphy2

#ключ 18b21fd284c1dc3b756bb051569f24c7b30c2a2c3c8ebc44695bd062fb13b6c9ac7b1782bd9835791e3de
#6954926

players_list = []
players = {}
flags_list = ['Россия', 'Турция', 'Китай', 'Германия', 'Испания', 'Франция',
              'Великобритания', 'Италия', 'Япония', 'Корея', 'США', 'Украина',
              'Австрия', 'Австралия', 'Бельгия', 'Бразилия', 'Канада', 'Швейцария',
              'Чили', 'Дания', 'Финляндия', 'Гонконг', 'Индонезия',
              'Ирландия', 'Индия', 'Мексика', 'Нидерланды', 'Норвегия',
              'Польша', 'Португалия', 'Аравия', 'Швеция', 'Сингапур', 'Вьетнам',
              'Казахстан', 'Беларусь', 'Израиль']

FLAGS = {'Россия': ['&#127479;&#127482;', '🇷🇺'],
         'Турция': ['&#127481;&#127479;', '🇹🇷'],
         'Китай': ['&#127464;&#127475;' , '🇨🇳'],
         'Германия': ['&#127465;&#127466;' , '🇩🇪'],
         'Испания': ['&#127466;&#127480;' , '🇪🇸'],
         'Франция': ['&#127467;&#127479;' , '🇫🇷'],
         'Великобритания': ['&#127468;&#127463;' , '🇬🇧'],
         'Италия': ['&#127470;&#127481;' , '🇮🇹'],
         'Япония': ['&#127471;&#127477;' , '🇯🇵'],
         'Корея': ['&#127472;&#127479;' , '🇰🇷'],
         'США': ['&#127482;&#127480;' , 'США'],
         'Украина': ['&#127482;&#127462;' , '🇺🇦'],
         'Австрия': ['&#127462;&#127481;' , '🇦🇹'],
         'Австралия': ['&#127462;&#127482;' , '🇦🇺'],
         'Бельгия': ['&#127463;&#127466;' , '🇧🇪'],
         'Бразилия': ['&#127463;&#127479;' , '🇧🇷'],
         'Канада': ['&#127464;&#127462;' , '🇨🇦'],
         'Швейцария': ['&#127464;&#127469;' , '🇨🇭'],
         'Чили': ['&#127464;&#127473;' , '🇨🇱'],
         'Дания': ['&#127465;&#127472;' , '🇩🇰'],
         'Финляндия': ['&#127467;&#127470;' , '🇫🇮'],
         'Гонконг': ['&#127469;&#127472;' , '🇭🇰'],
         'Индонезия': ['&#127470;&#127465;' , '🇮🇩'],
         'Ирландия': ['&#127470;&#127466;' , '🇮🇪'],
         'Индия': ['&#127470;&#127475;' , '🇮🇳'],
         'Мексика': ['&#127474;&#127485;' , '🇲🇽'],
         'Нидерланды': ['&#127475;&#127473;' , '🇳🇱'],
         'Норвегия': ['&#127475;&#127476;' , '🇳🇴'],
         'Польша': ['&#127477;&#127473;' , '🇵🇱'],
         'Португалия': ['&#127477;&#127481;' , '🇵🇹'],
         'Аравия': ['&#127480;&#127462;	' , '🇸🇦'],
         'Швеция': ['&#127480;&#127466;' , '🇸🇪'],
         'Сингапур': ['&#127480;&#127468;' , '🇸🇬'],
         'Вьетнам': ['&#127483;&#127475;' , '🇻🇳 '],
         'Казахстан': ['&#127472;&#127487;' , '🇰🇿'],
         'Беларусь': ['&#127463;&#127486;' , '🇧🇾'],
         'Израиль': ['&#127470;&#127473;' , '🇮🇱']
         }

tokenn = '04e018fecf9457e70da517b12f2688fe284dca632b9b5e47bdcd59530de1a08a6cac24778b0e67fb91a78'
token = '18b21fd284c1dc3b756bb051569f24c7b30c2a2c3c8ebc44695bd062fb13b6c9ac7b1782bd9835791e3de'

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random.randint(1, 2147483647)})

def write_msg2(user_id, message, keyboard):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random.randint(1, 2147483647), "keyboard": keyboard})

def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

keyboard = {
    "one_time": True,
    "buttons": [

    [get_button(label="Кнопка 1", color="positive")],
    [get_button(label="Кнопка 2", color="negative")],
    [get_button(label="Кнопка 3", color="primary")],
    [get_button(label="Кнопка 4", color="default")]

    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

def new_user(idd):
    global players
    players[idd] = {'great': 0, 'wait_for_answer': False, 'wait_for_answer_flag': False}

def new_keys_countries(need):
    global flags_list
    global keyboard
    nums = [flags_list.index(need)]
    while len(nums) < 4:
        new = random.randint(0, 36)
        if not new in nums:
            nums.append(new)
    random.shuffle(nums)
    keyboard = {
        "one_time": True,
        "buttons": [

        [get_button(label=flags_list[nums[0]], color="positive")],
        [get_button(label=flags_list[nums[1]], color="negative")],
        [get_button(label=flags_list[nums[2]], color="primary")],
        [get_button(label=flags_list[nums[3]], color="default")]

        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

def menu(first=False):
    #global flags_list
    global keyboard
    keyboard = {
        "one_time": True,
        "buttons": [

        [get_button(label='хочу угадать флаг', color="positive")],
        [get_button(label='хочу угадать страну', color="positive")],
        [get_button(label='пока (узнать баллы)', color="default")]
        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    mes = "ну что, ещё по одной?"
    if first:
        mes = 'привет. я умею немного, зато я лапочка :3\nну что, сыграем?'
        mes += '\nучти, я считаю баллы: правильный ответ +1, неправильный -1'
    write_msg2(event.user_id, mes, keyboard)

def new_keys_flags(need):
    global flags_list
    global keyboard
    nums = [flags_list.index(need)]
    while len(nums) < 4:
        new = random.randint(0, 36)
        if not new in nums:
            nums.append(new)
    random.shuffle(nums)
    keyboard = {
        "one_time": True,
        "buttons": [

        [get_button(label=FLAGS[flags_list[nums[0]]][0], color="positive")],
        [get_button(label=FLAGS[flags_list[nums[1]]][0], color="negative")],
        [get_button(label=FLAGS[flags_list[nums[2]]][0], color="primary")],
        [get_button(label=FLAGS[flags_list[nums[3]]][0], color="default")]

        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))


def nomn_case(word):
    morph = pymorphy2.MorphAnalyzer()
    txt = morph.parse(word)[0]
    w = txt.inflect({'sing', 'nomn'})
    return w.word[0].upper() + w.word[1:]

def gent_case(word):
    morph = pymorphy2.MorphAnalyzer()
    txt = morph.parse(word)[0]
    w = txt.inflect({'sing', 'gent'})
    return w.word[0].upper() + w.word[1:]

# авторизация
vk = vk_api.VkApi(token=token)
#print(vk.token)
longpoll = VkLongPoll(vk)

wait_for_answer, wait_for_answer_flag = False, False
right_answer = ''
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.user_id not in players_list:
                players_list.append(event.user_id)
                new_user(event.user_id)

            request = event.text
            new_mes = str(event.user_id) + ' ' + request
            print(new_mes)

            if request[:6].lower() == "привет":
                mes = 'привет, ' + datas(event.user_id)[0]['first_name']
                write_msg(event.user_id, mes)
                #write_msg(event.user_id, "я многое умею:")
                menu(first=True)

            elif request[:4] == "пока":
                morph = pymorphy2.MorphAnalyzer()
                res = morph.parse('баллы')[0]
                count = players[event.user_id]['great']
                players[event.user_id]['great'] = 0
                mes = 'ну пока, ' + datas(event.user_id)[0]['first_name']
                mes += '\nты набрал(-a) ' + str(count) + ' '
                mes += res.make_agree_with_number(count).word
                write_msg(event.user_id, mes)

            elif players[event.user_id]['wait_for_answer'] and request == right_answer:
                write_msg(event.user_id, "браво! абсолютно верно!")
                players[event.user_id]['great'] = players[event.user_id]['great'] + 1
                players[event.user_id]['wait_for_answer'] = False
                print(players[event.user_id]['wait_for_answer'])
                menu()

            elif (players[event.user_id]['wait_for_answer'] or players[event.user_id]['wait_for_answer_flag']) and request[:6] == 'покажи':
                write_msg(event.user_id, "каков наглец!")
                players[event.user_id]['wait_for_answer'] = False
                players[event.user_id]['wait_for_answer_flag'] = False
                menu()

            elif players[event.user_id]['wait_for_answer']:
                write_msg(event.user_id, "сам ты " + request)
                wait_for_answer = False
                write_msg(event.user_id, "не обижайся, я любя)")
                players[event.user_id]['great'] = players[event.user_id]['great'] - 1
                menu()

            elif players[event.user_id]['wait_for_answer_flag'] and request == right_answer:
                write_msg(event.user_id, "браво! абсолютно верно!")
                players[event.user_id]['great'] = players[event.user_id]['great'] + 1
                players[event.user_id]['wait_for_answer_flag'] = False
                menu()

            elif players[event.user_id]['wait_for_answer_flag']:
                write_msg(event.user_id, 'неа: ' + right_answer)
                players[event.user_id]['great'] = players[event.user_id]['great'] - 1
                players[event.user_id]['wait_for_answer_flag'] = False
                menu()

            elif request[:12].lower() == "покажи флаг ":
                country = nomn_case(request[12:])
                if country not in flags_list:
                    write_msg(event.user_id, 'не знаю такой страны((')
                    menu()
                else:
                    new_keys_countries(country)
                    write_msg(event.user_id, FLAGS[country][0])

            elif request.lower() == "хочу угадать страну":
                country = flags_list[random.randint(0, 36)]
                new_keys_countries(country)
                write_msg2(event.user_id, FLAGS[country][0], keyboard)
                players[event.user_id]['wait_for_answer_flag'] = True
                right_answer = country

            elif request.lower() == "хочу угадать флаг":
                country = flags_list[random.randint(0, 36)]
                new_keys_flags(country)
                ask = 'где флаг ' + gent_case(country) + '?'
                write_msg2(event.user_id, ask, keyboard)
                players[event.user_id]['wait_for_answer_flag'] = True
                right_answer = FLAGS[country][1]
            else:
                write_msg(event.user_id, "сам ты " + request)