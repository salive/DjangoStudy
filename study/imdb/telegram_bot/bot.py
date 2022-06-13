from email import message
from django.conf import settings
from psycopg2 import DatabaseError
from telebot import TeleBot, types
from imdb.utils.telegram.user_utils import check_registered_user, user_register, get_username_by_telegram_id
from imdb.utils.telegram.user_shows import get_user_shows_list, format_show_details, mark_show_as_seen
from imdb.utils.kinopoisk_api import KP_API
from imdb.utils.shows_add_utils import add_usershow, check_usershow_exists


bot = TeleBot(settings.TELEGRAM_API_KEY)


def default_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    library_button = types.KeyboardButton('Моя библиотека')
    search_button = types.KeyboardButton('Искать')
    markup.add(library_button, search_button)
    return markup


@bot.callback_query_handler(func=lambda call: True)
def handle_call(call):
    action = call.data.split()[0]
    try:
        data = call.data.split()[1]
    except:
        pass

    match action:
        case 'show_details':
            details = KP_API.parse_response(data, 'show_details')
            markup = types.InlineKeyboardMarkup()
            if check_usershow_exists(call.from_user.id, data):
                inline_button = types.InlineKeyboardButton(
                    'Посмотрел!', callback_data=f'mark_seen {data}')
            else:
                inline_button = types.InlineKeyboardButton(
                    'Хочу посмотреть!', callback_data=f'add {data}')
            markup.add(inline_button)
            bot.send_photo(call.from_user.id,
                           *format_show_details(details), reply_markup=markup)
            bot.answer_callback_query(callback_query_id=call.id)

        case 'mark_seen':
            msg = bot.send_message(
                call.from_user.id, 'Ты можешь оценить фильм от 1 до 10')
            bot.register_next_step_handler(
                msg, mark_as_seen, call.from_user.id, data)

            bot.answer_callback_query(callback_query_id=call.id)
        case 'add':
            try:
                result = add_usershow(call.from_user.id, data)
                if result:
                    bot.send_message(call.from_user.id,
                                     'Добавлено!', reply_markup=default_markup())
                else:
                    bot.send_message(call.from_user.id,
                                     'Упс! Уже есть в твоем списке', reply_markup=default_markup())
                bot.answer_callback_query(callback_query_id=call.id)
            except DatabaseError:
                bot.send_message(call.from_user.id,
                                 'Что-то пошло не так =(', reply_markup=default_markup())


def mark_as_seen(message, user_id, show_id):
    rating = 0
    if message.text.isnumeric() and 1 <= int(message.text) <= 10:
        rating = message.text
    mark_show_as_seen(user_id, show_id, rating)
    bot.send_message(user_id, f'Оценка сохранена!',
                     reply_markup=default_markup())


def find_show(message):
    target = message.text
    shows = KP_API.parse_response(target, 'keyword')
    markup = types.InlineKeyboardMarkup()
    for show in shows:
        details_button = types.InlineKeyboardButton(
            text=f'{show[2]}: {show[3]}', callback_data=f'show_details {show[0]}')
        markup.add(details_button)
    bot.send_message(message.from_user.id,
                     'Вот, что я нашел:', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_logic(message):
    match message.text:
        case '/start':
            if not check_registered_user(message.from_user.id):
                bot.send_message(message.from_user.id,
                                 "Привет, похоже мы еще не знакомы! Как тебя зовут?")
                bot.register_next_step_handler(message, register)
            else:
                bot.send_message(message.from_user.id,
                                 f"Привет, {get_username_by_telegram_id(message.from_user.id)}", reply_markup=default_markup())

            def register(message):
                name = message.text
                try:
                    user_register(message.from_user.id, name)
                    bot.send_message(message.from_user.id,
                                     f'Добро пожаловать, {name}', reply_markup=default_markup())
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.from_user.id,
                                     "Что-то пошло не так, сейчас разберусь")

        case '/shows' | 'Моя библиотека':
            try:
                shows = get_user_shows_list(message.from_user.id)
                if shows:
                    markup = types.InlineKeyboardMarkup()
                    for show in shows:
                        details_button = types.InlineKeyboardButton(
                            text=f'{show.show.title}: {show.show.year}', callback_data=f'show_details {show.show.id}')
                        markup.add(details_button)
                    bot.send_message(message.from_user.id,
                                     f'Это список твоих фильмов к просмотру:', reply_markup=markup)
                else:
                    bot.send_message(message.from_user.id,
                                     f'Похоже список пуст, давай что-нибудь добавим! Введи название интересующего тебя фильма или сериала', reply_markup=types.ReplyKeyboardRemove())
                    bot.register_next_step_handler(
                        message, find_show)
            except:
                bot.send_message(message.from_user.id,
                                 "Что-то пошло не так, сейчас разберусь")

        case '/find' | 'Искать':
            bot.send_message(message.from_user.id,
                             f'Что ищем?', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(
                message, find_show)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=1)
