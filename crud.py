import string, random
from db import engine
from sqlalchemy.orm import sessionmaker
from models import User, Check
from random import randint


session = sessionmaker(bind = engine)


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def create_user(s: session(), user: dict): # Функция создания юзера
    user = User(telid = user['telid'], username = user['username'],  name = user['name'], sphere = user['sphere'], ed_name = user['ed_name'], event_descr = user['event_descr'], hashes = user['hashes'], name_img = user['name_img'], choose = user['choose_find'])
    s.add(user)
    s.commit()


def get_user_by_img(s: session(), name_img: str):
    zn = s.query(User).filter(User.name_img == name_img).group_by(User).first()
    return zn


def check_user(s: session(), telid:str): # Функция проверки пользователя на зарегестрированность
    zn = s.query(User).filter(User.telid == telid).group_by(User).first()
    return zn


def get_random_user(users: dict): # Функция получения рандомного пользователя
    return users[randint(0, len(users) - 1)]


def check_use(s: session(), us_telid: str, telid: str): # Функция проверка на просмотренность
    used = s.query(Check).filter(Check.us_telid == us_telid).all()

    for row in used:
        print(row.telid)
        if row.telid == telid or us_telid == telid:
            return True
    if us_telid != telid:
        return False
    else:
        return True
    

def get_all(s: session()):# Функция получения всех юзеров
    users = []
    user = {}
    for row in s.query(User).all():
        user['telid'] = row.telid
        user['name_img'] = row.name_img
        user['username'] = row.username
        user['name'] = row.name
        user['sphere'] = row.sphere
        user['ed_name'] = row.ed_name
        user['event_descr'] = row.event_descr
        users.insert(len(users), user)
        user = {}
    return users


def create_used(s: session(), used: str, us_telid: str): # Функция добавление просмотренного пользователя
    used = Check(telid = used, us_telid = us_telid)
    s.add(used)
    s.commit()


def get_used_us(s: session(), us_telid: str): # Функция получения всех просмотренных пользователей у юзера
    zn = s.query(Check).filter(Check.us_telid == us_telid).group_by(Check).all()
    k = 0
    for row in zn:
        k += 1
    return k


def del_viewed(s: session(), us_telid: str):
    s.query(Check).filter(Check.us_telid == us_telid).delete()


def check_correct_tags(tags_str: str):
    tag_list = tags_str.split(' ')
    for i in tag_list:
        if i[0] != '#':
            return False
    return True
