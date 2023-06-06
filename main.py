import telebot
from telebot import types
from crud import generate_random_string, create_user, get_user_by_img, check_user, get_all, get_random_user, check_use, create_used, get_used_us, del_viewed, check_correct_tags
from sqlalchemy.orm import sessionmaker
from db import engine


bot = telebot.TeleBot('6051674846:AAEHKq9wv6Hw9jp-WkwtoZUETjfAdKSlcGE')


session = sessionmaker(bind=engine)
s = session()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    prog = types.KeyboardButton(text='Поехали! 🚀🚀🚀') # Кнопка Поехали, которая будет стартовать регистрацию
    markup.add(prog)
    # Отправление приветственного сообщения с информацией о боте
    bot.send_message(message.chat.id, f'Приветствую тебя {message.from_user.first_name} в чат-боте TeamFinder\n \nЭтот бот создан для того, чтобы ты мог найти себе команду, например, для участия в хакатонах, конкурсах или создания совместных проектов\n\n Для начала заполни небольшую анкету о себе, чтобы мы смогли подобрать самого подходящего пользователя: )\n\nЕсли вам нужна помощь в использовании, напишите /help', reply_markup=markup)


@bot.message_handler(content_types = ['text', 'photo'])
def main(message):
    
    

    if message.text == 'Поехали! 🚀🚀🚀':
            user={}
            c_u = check_user(s, message.from_user.id) # Проверка зарегистрирован ли пользователь
            if c_u:
                r_k = types.ReplyKeyboardRemove()
                
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                prog = types.KeyboardButton(text='ИСКАТЬ 🔎')
                markup.add(prog)
                bot.send_message(message.chat.id, 'Ты уже зарегистрирован!', reply_markup = r_k)
                bot.send_message(message.chat.id, 'Но ничего страшного, ты можешь начать искать', reply_markup = markup)
            else:
                user['telid'] = message.from_user.id
                user['username'] = message.from_user.username

                r_k = types.ReplyKeyboardRemove()
                msg_1 = bot.send_message(message.chat.id, 'Как тебя зовут (Сначала введите фамилию, потом имя через пробел)?', reply_markup = r_k)
                bot.register_next_step_handler(msg_1, name_handler, user)
    elif message.text == "ИСКАТЬ 🔎":
        c_u = check_user(s, message.from_user.id) # Проверка зарегистрирован ли пользователь
        if c_u:

            users = get_all(s) # Получение информации о всех пользователях
            last = False
            while True: # в цикле ждем пока выпадет рандомный пользователь, которого еще не было( вся инфа хранится в бд )
                user = get_random_user(users)
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("ОБЩАТЬСЯ!", url=f'https://t.me/{user["username"]}')# Ссылка на аккаунт пользоватлея
                print(user['name'])
                if not(check_use(s, message.from_user.id,user['telid'])):
                    create_used(s, user['telid'], message.from_user.id)
                    markup.add(button1)
                    if len(users) == get_used_us(s, message.from_user.id):
                        last=True
                    break
                elif len(users) == get_used_us(s, message.from_user.id):
                    break
            print(get_used_us(s, message.from_user.id))
            if len(users) == get_used_us(s, message.from_user.id) and not(last): # Если кол-во просмотренных пользователей равно кол-ву всех, значит все пользователи просмотрены
                markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                prog_1 = types.KeyboardButton(text='ПЕРЕСМОТРЕТЬ 🔄')
                markup_1.add(prog_1)
                bot.send_message(message.chat.id, 'К сожалению, пользователи кончились, ты просмотрел всех. Вернись чуть позже \n\n Но если хочешь просмотреть их еще раз, нажми кнопку ПЕРЕСМОТРЕТЬ, потом у тебя появится кнопка ИСКАТЬ, и ты сможешь снова просмотреть пользователей', reply_markup=markup_1)

            else:
                bot.send_photo(message.chat.id, photo=open(user['name_img'], 'rb'))
                bot.send_message(message.chat.id, f"{user['name']}\n\nСфера деятельности: {user['sphere']}\n\nУчебное заведение: {user['ed_name']}\n\n{user['event_descr']}\n\n", reply_markup = markup)
        else: 
            bot.send_message(message.chat.id, 'Ты еще не зарегистрирован! Но ничего страшного, ты можешь начать регистрацию, нажав ПОЕХАЛИ') # Выводим, если пользователь не зареган
    elif  message.text == 'ПЕРЕСМОТРЕТЬ 🔄':
        del_viewed(s, message.from_user.id)
        markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        pro = types.KeyboardButton(text='ИСКАТЬ 🔎')
        markup_2.add(pro)
        bot.send_message(message.chat.id, 'Отлично, ты можешь снова просмотреть пользователей!', reply_markup = markup_2)

def name_handler(message, user):
    name = message.text
    user['name'] = name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    it_button = types.KeyboardButton(text='IT')
    dis_button = types.KeyboardButton(text='Дизайн')
    inj_button = types.KeyboardButton(text='Инженерия')
    gur_button = types.KeyboardButton(text='Журналистика')
    vol_button = types.KeyboardButton(text='Волонтер')
    markup.add(it_button, dis_button, inj_button, gur_button, vol_button)
    msg_1 = bot.send_message(message.chat.id, 'Выбери сферу своей увлеченности', reply_markup=markup)
    bot.register_next_step_handler(msg_1, sphere_handler, user)


def sphere_handler(message, user):
    markup = types.ReplyKeyboardRemove()
    sphere = message.text
    user['sphere'] = sphere
    msg_2 = bot.send_message(message.chat.id, 'Напишите название своего учебного заведения( университета, школы, коледжа )?', reply_markup=markup)
    bot.register_next_step_handler(msg_2, educate_handler, user)


def educate_handler(message, user):
    ed_name = message.text
    user['ed_name'] = ed_name
    msg_3 = bot.send_message(message.chat.id, 'Опишите свой проект, конкурс, хакатон, куда вы ищите единомышленника')
    bot.register_next_step_handler(msg_3, event_handler, user)


def event_handler(message, user):
    event_descr = message.text
    user['event_descr'] = event_descr
    msg_4 = bot.send_message(message.chat.id, 'Напишите хэштеги для конкретного конкурса, которые помогут нам найти вам наиболее подходящего человека \n\n Пример: #КонкурсОтРосАтома #Делайдобро')
    bot.register_next_step_handler(msg_4, hash_tag_handler, user)                     
    
    

def hash_tag_handler(message, user):
    hashes = message.text
    if check_correct_tags(hashes):

        user['hashes'] = hashes
        msg_5 = bot.send_message(message.chat.id, 'И последнее, загрузи свою фотку!')
        bot.register_next_step_handler(msg_5, add_photo, user)
    else:
        msg_n = bot.send_message(message.chat.id, 'Некоректно введены хэштеги, попробуйте еще раз')
        bot.register_next_step_handler(msg_n, hash_tag_handler, user)


def add_photo(message, user):
    if message.content_type == 'photo':
        while True:
            random_name = generate_random_string(16)
            if get_user_by_img(s, f'static/{random_name}.jpg') is None:
                break
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        user['name_img'] = f'static/{random_name}.jpg'
        with open(f"static/{random_name}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        print(user)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        random_button = types.KeyboardButton(text='РАНДОМ')
        hash_button = types.KeyboardButton(text='По хэштегам')
        sphere_button = types.KeyboardButton(text='По сфере')
        markup.add(random_button, hash_button, sphere_button)
        msg_6 = bot.send_message(message.chat.id, f"Ты успешно прошёл регистрацию! Следующий шаг - нахождение единомышленников, для этого нужно указать, как мы будем искать!", reply_markup=markup)
        bot.register_next_step_handler(msg_6, choose_find_handler, user)
    else:
        msg8 = bot.send_message(message.chat.id, f"Ты отправил что-то, но явно не фото, попробуй еще раз : )")
        bot.register_next_step_handler(msg8, add_photo, user)


def choose_find_handler(message, user):
    choose_find = message.text
    user['choose_find'] = choose_find
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    prog = types.KeyboardButton(text='ИСКАТЬ 🔎')
    markup.add(prog)
    create_user(s, user) # Функция добавления пользователя в БД
    bot.send_message(message.chat.id, f"Отлично!!! Можно начинать поиск!", reply_markup=markup)


bot.polling(none_stop=True) # Запускаем бот
