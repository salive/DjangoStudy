from xml.dom.domreg import registered
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import telebot
from imdb.utils.telegram.auth import check_registered_user, user_register
from imdb.utils.telegram.user_shows import get_user_shows_list, format_show_message
from imdb.utils.kinopoisk_api import KP_API


class Command(BaseCommand):
    help = 'Shows telegram bot'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TELEGRAM_API_KEY)

        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            if not check_registered_user(message.from_user.id):
                def get_name(message):
                    name = message.text
                    try:
                        user_register(message.from_user.id, name)
                        bot.send_message(message.from_user.id,
                                         f'Добро пожаловать, {name}')
                    except:
                        bot.send_message(message.from_user.id,
                                         "Что-то пошло не так, сейчас разберусь")
                bot.send_message(message.from_user.id,
                                 "Привет, похоже мы еще не знакомы! Как тебя зовут?")
                bot.register_next_step_handler(message, get_name)

            def find_show(message):
                target = message.text
                print(target)
                shows = KP_API.parse_response(target, 'keyword')
                bot.send_message(message.from_user.id,
                                 f'Вот, что я нашел:')
                for show in shows:
                    bot.send_photo(message.from_user.id,
                                   *format_show_message(show))

            match message.text:

                case "/shows":
                    try:
                        shows = get_user_shows_list(message.from_user.id)
                        if shows:
                            bot.send_message(message.from_user.id,
                                             f'Это список твоих фильмов к просмотру:')
                        else:
                            bot.send_message(message.from_user.id,
                                             f'Похоже список пуст, давай что-нибудь добавим: /find ')
                    except:
                        bot.send_message(message.from_user.id,
                                         "Что-то пошло не так, сейчас разберусь")

                case "/find":
                    bot.send_message(message.from_user.id,
                                     f'Введи название или хотя бы его часть')
                    bot.register_next_step_handler(message, find_show)

        bot.polling(none_stop=True, interval=1)
