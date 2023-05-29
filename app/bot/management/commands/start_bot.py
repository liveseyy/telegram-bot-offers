import logging

from django.core.management.base import BaseCommand

from aiogram import Dispatcher, executor

from bot.bot import bot

from bot.bot_handlers.start_menu import register_start_and_menu_on_dispatcher
from bot.bot_handlers.create_observer import register_create_observer_on_dispatcher
from bot.bot_handlers.show_observers import register_show_my_observers
from bot.bot_handlers.unknown_command import register_handle_unknown_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.basicConfig(level=logging.DEBUG)

        bot_dispatcher = Dispatcher(bot)

        register_start_and_menu_on_dispatcher(dispatcher=bot_dispatcher)
        register_create_observer_on_dispatcher(dispatcher=bot_dispatcher)
        register_show_my_observers(dispatcher=bot_dispatcher)
        register_handle_unknown_command(dispatcher=bot_dispatcher)

        executor.start_polling(bot_dispatcher, skip_updates=True)
