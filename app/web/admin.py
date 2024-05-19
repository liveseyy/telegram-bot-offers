from django.contrib import admin
from parse_offers.models import AvitoCategory, AvitoUserOfferWatcherFilter, AvitoUserOfferWatcher
from bot.models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass


@admin.register(AvitoCategory)
class AvitoCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(AvitoUserOfferWatcherFilter)
class AvitoUserOfferWatcherFilterAdmin(admin.ModelAdmin):
    pass


@admin.register(AvitoUserOfferWatcher)
class AvitoUserOfferWatcherAdmin(admin.ModelAdmin):
    pass
