from xml.dom.domreg import registered
from django.core.management.base import BaseCommand, CommandError
import imdb.telegram_bot.bot as bot


class Command(BaseCommand):
    help = 'Shows telegram bot'

    def handle(self, *args, **options):
        bot.bot.polling(none_stop=True, interval=1)
