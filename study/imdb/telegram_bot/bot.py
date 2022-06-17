from collections import namedtuple
from enum import Enum
from functools import wraps
from django.conf import settings
from psycopg2 import DatabaseError
from telebot import TeleBot, types
from imdb.services.telegram.user_utils import check_registered_user, user_register, find_show
from imdb.services.telegram.user_shows import format_show_details,\
    mark_show_as_seen, delete_show, check_show_is_seen, get_user_rating, subscribe_on_updates, get_episode_info, check_show_is_series
from imdb.services.telegram.utils import process_callback_data
from imdb.services.telegram.markups import default_keyboard_markup, list_inline_markup, delete_confirmation_markup, \
    details_inline_markup, seasons_inline_markup, episodes_inline_markup, episode_info_inline_markup
from imdb.services.kinopoisk_api import KP_API, KPResponse
from imdb.services.shows_add_utils import add_usershow, check_usershow_exists


class MyTeleBot(TeleBot):
    '''
    Custom class based on TeleBot class
    '''

    def __init__(self):
        self.authenticated_users = {}
        super().__init__(settings.TELEGRAM_API_KEY)

    class Commands(Enum):
        find = 'Искать'
        watch_list = 'Список к просмотру'
        my_films = 'Мои фильмы'
        my_series = 'Мои cериалы'

    @staticmethod
    def auth_check(fn):
        '''
        Check user authentication decorator
        '''
        @wraps(fn)
        def inner(message):
            if not bot.authenticated_users.get(message.from_user.id, False):
                if not check_registered_user(message.from_user.id):
                    bot.send_message(message.from_user.id,
                                     "Привет, похоже мы еще не знакомы! Как тебя зовут?")
                    bot.register_next_step_handler(message, user_register)
            return fn(message)
        return inner


bot = MyTeleBot()


@bot.callback_query_handler(func=lambda call: True)
def handle_call(call):
    bot.clear_step_handler(call.message)
    data = process_callback_data(call.data)
    match data.action:
        case 'show_details':
            details = KP_API.parse_response(data.data, 'show_details')
            bot.send_photo(call.from_user.id,
                           *format_show_details(details), reply_markup=details_inline_markup(call.from_user.id, data.data, details.is_series))
            bot.answer_callback_query(callback_query_id=call.id)

        case 'next_page':
            current_page = int(data.data)
            bot.edit_message_reply_markup(
                call.message.chat.id, call.message.id, reply_markup=list_inline_markup(call.from_user.id, current_page, data.filter))
            bot.answer_callback_query(callback_query_id=call.id)

        case 'mark_seen':
            msg = bot.send_message(
                call.from_user.id, 'Ты можешь поставить оценку от 1 до 10')
            bot.register_next_step_handler(
                msg, mark_as_seen, call.from_user.id, data.data)
            bot.edit_message_reply_markup(
                call.message.chat.id, call.message.id, reply_markup=details_inline_markup(call.from_user.id, data.data))
            bot.answer_callback_query(callback_query_id=call.id)

        case 'add':
            result = add_usershow(call.from_user.id, data.data)
            if result:
                bot.edit_message_reply_markup(
                    call.message.chat.id, call.message.id, reply_markup=details_inline_markup(call.from_user.id, data.data, check_show_is_series(data.data)))
            else:
                bot.send_message(call.from_user.id,
                                 'Упс! Уже есть в твоем списке', reply_markup=default_keyboard_markup())

            bot.answer_callback_query(callback_query_id=call.id)

        case 'delete':
            if not data.filter:
                bot.send_message(call.from_user.id, 'Точно удаляем?',
                                 reply_markup=delete_confirmation_markup(data.data, call.message.id))
                bot.answer_callback_query(callback_query_id=call.id)
                return

            if data.filter == 'confirmed':
                delete_show(call.from_user.id, data.data)
                bot.answer_callback_query(
                    callback_query_id=call.id, show_alert=True, text='Удалено')
            bot.delete_message(call.message.chat.id, call.message.id)

        case 'seasons':
            if data.filter == 'back':
                bot.edit_message_reply_markup(
                    call.message.chat.id, call.message.id, reply_markup=details_inline_markup(call.from_user.id, data.data, True))
                bot.answer_callback_query(callback_query_id=call.id)
                return

            bot.edit_message_reply_markup(
                call.message.chat.id, call.message.id, reply_markup=seasons_inline_markup(data.data))
            bot.answer_callback_query(callback_query_id=call.id)

        case 'season_info':
            if data.filter == 'back':
                bot.edit_message_reply_markup(
                    call.message.chat.id, call.message.id, reply_markup=seasons_inline_markup(data.data))
                bot.answer_callback_query(callback_query_id=call.id)
                return
            bot.edit_message_reply_markup(
                call.message.chat.id, call.message.id, reply_markup=episodes_inline_markup(data.data, data.id_1))
            bot.answer_callback_query(callback_query_id=call.id)

        case 'episode_info':
            if data.filter == 'back':
                bot.edit_message_reply_markup(
                    call.message.chat.id, call.message.id, reply_markup=episodes_inline_markup(data.data, data.id_1))
                bot.answer_callback_query(callback_query_id=call.id)
                return
            episode = get_episode_info(data.data)
            bot.send_message(
                call.from_user.id,
                text=f"\n{episode.titleRu} | {episode.titleEn}\n\n"
                f"Дата выхода: {episode.air_date}\n\n"
                f"{episode.description}\n\n",
                reply_markup=episode_info_inline_markup(data.data, data.id_1, data.id_2))
            bot.answer_callback_query(callback_query_id=call.id)

        case 'subscribe':
            if data.filter == 'on':
                if subscribe_on_updates(call.from_user.id, data.data, True):
                    bot.edit_message_reply_markup(
                        call.message.chat.id, call.message.id, reply_markup=details_inline_markup(call.from_user.id, data.data, True))
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                              text='Готово! Теперь я буду присылать тебе уведомление в день выхода новой серии этого сериала.')
            if data.filter == 'off':
                if subscribe_on_updates(call.from_user.id, data.data, False):

                    bot.edit_message_reply_markup(
                        call.message.chat.id, call.message.id, reply_markup=details_inline_markup(call.from_user.id, data.data, True))
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                              text='Готово! Уведомления больше не будут приходить')


def mark_as_seen(message, user_id, show_id):
    rating = 0
    if message.text.isnumeric() and 1 <= int(message.text) <= 10:
        rating = message.text
    mark_show_as_seen(user_id, show_id, rating)
    bot.send_message(user_id, f'Оценка сохранена!',
                     reply_markup=default_keyboard_markup())


@bot.message_handler(content_types=['text'])
@bot.auth_check
def bot_logic(message):
    match message.text:
        case '/start':
            bot.send_message(message.from_user.id,
                             f'Давай начнем!', reply_markup=default_keyboard_markup())

        case bot.Commands.watch_list.value:
            markup = list_inline_markup(message.from_user.id, 1, 'unseen')
            if markup:
                bot.send_message(message.from_user.id,
                                 f'Это твой список к просмотру:', reply_markup=markup)
            else:
                bot.send_message(message.from_user.id,
                                 f'Список пуст',
                                 reply_markup=default_keyboard_markup())

        case bot.Commands.my_films.value:
            markup = list_inline_markup(message.from_user.id, 1, 'my_films')
            if markup:
                bot.send_message(message.from_user.id,
                                 f'Это твой список фильмов:', reply_markup=markup)
            else:
                bot.send_message(message.from_user.id,
                                 f'Список пуст',
                                 reply_markup=default_keyboard_markup())

        case bot.Commands.my_series.value:
            markup = list_inline_markup(message.from_user.id, 1, 'my_series')
            if markup:
                bot.send_message(message.from_user.id,
                                 f'Это твой список сериалов:', reply_markup=markup)
            else:
                bot.send_message(message.from_user.id,
                                 f'Список пуст',
                                 reply_markup=default_keyboard_markup())

        case bot.Commands.find.value:
            bot.send_message(message.from_user.id,
                             f'Что ищем?', reply_markup=default_keyboard_markup())
            bot.register_next_step_handler(
                message, find_show)
        case _:

            bot.send_message(message.from_user.id,
                             f'Я не знаю такой команды, извини', reply_markup=default_keyboard_markup())


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=1)
