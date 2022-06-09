from django.conf import settings
from telebot import TeleBot, types
from imdb.utils.telegram.user_utils import check_registered_user, user_register, get_username_by_telegram_id
from imdb.utils.telegram.user_shows import get_user_shows_list, format_show_details
from imdb.utils.kinopoisk_api import KP_API


class TelegramBot:
    def __init__(self):
        self.bot = TeleBot(settings.TELEGRAM_API_KEY)

        @self.bot.message_handler(commands=['start'])
        def start(message):
            if not check_registered_user(message.from_user.id):
                self.bot.send_message(message.from_user.id,
                                      "Привет, похоже мы еще не знакомы! Как тебя зовут?")
                self.bot.register_next_step_handler(message, register)
            else:
                self.bot.send_message(message.from_user.id,
                                      f"Привет, {get_username_by_telegram_id(message.from_user.id)}")

        @self.bot.message_handler(commands=['register'])
        def register(message):
            name = message.text
            try:
                user_register(message.from_user.id, name)
                self.bot.send_message(message.from_user.id,
                                      f'Добро пожаловать, {name}')
            except Exception as ex:
                print(ex)
                self.bot.send_message(message.from_user.id,
                                      "Что-то пошло не так, сейчас разберусь")

        @self.bot.callback_query_handler(func=lambda call: True)
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
                    details_button = types.InlineKeyboardButton(
                        text=f'Хочу посмотреть!', callback_data=f'add {data}')
                    markup.add(details_button)
                    self.bot.send_photo(call.from_user.id,
                                        *format_show_details(details), reply_markup=markup)
                case 'add':
                    markup = types.InlineKeyboardMarkup()
                    library_button = types.InlineKeyboardButton(
                        text=f'Перейти к моим фильмам', callback_data=f'library None')
                    search_button = types.InlineKeyboardButton(
                        text=f'Искать еще', callback_data=f'search None')
                    markup.add(library_button, search_button)
                    self.bot.send_message(call.from_user.id,
                                          'Добавлено!', reply_markup=markup)
                case 'search':
                    message = self.bot.send_message(
                        call.from_user.id, 'Что ищем?')
                    self.bot.register_next_step_handler(message, find_show)

        def find_show(message):
            target = message.text
            shows = KP_API.parse_response(target, 'keyword')
            markup = types.InlineKeyboardMarkup()
            for show in shows:
                details_button = types.InlineKeyboardButton(
                    text=f'{show[2]}: {show[3]}', callback_data=f'show_details {show[0]}')
                markup.add(details_button)
            self.bot.send_message(message.from_user.id,
                                  'Вот, что я нашел:', reply_markup=markup)

        @self.bot.message_handler(commands=['shows'])
        def shows(message):
            try:
                shows = get_user_shows_list(message.from_user.id)
                if shows:
                    self.bot.send_message(message.from_user.id,
                                          f'Это список твоих фильмов к просмотру:')
                else:
                    self.bot.send_message(message.from_user.id,
                                          f'Похоже список пуст, давай что-нибудь добавим! Введи название интересующего тебя фильма или сериала')
                    self.bot.register_next_step_handler(
                        message, find_show)
            except:
                self.bot.send_message(message.from_user.id,
                                      "Что-то пошло не так, сейчас разберусь")

        @self.bot.message_handler(commands=['find'])
        def find(message):
            self.bot.send_message(message.from_user.id,
                                  f'Что ищем?')
            self.bot.register_next_step_handler(
                message, find_show)

    def start_polling(self):
        self.bot.polling(none_stop=True, interval=1)
