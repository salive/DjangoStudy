from xml.dom.domreg import registered
from django.core.management.base import BaseCommand, CommandError
from imdb.telegram_bot.bot import TelegramBot


class Command(BaseCommand):
    help = 'Shows telegram bot'

    def handle(self, *args, **options):
        bot = TelegramBot()
        bot.start_polling()
