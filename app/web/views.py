from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.views import View

from common.shortcuts import CustomSchemeRedirect
from common.utils import method_cache_key

from parse_offers.avito_cars_brands_models import CAR_MODELS_BY_BRANDS
from parse_offers.models import AvitoUserOfferWatcher
from bot.models import TelegramUser
from bot.bot_handlers.create_observer import delete_cache_stage_create_watcher
from bot.bot_handlers.start_menu.handle_menu import send_menu_as_answer_on_message
from bot.bot import bot

from web.forms import OfferWatchersForm
from web.validation.watchers_edit import parse_watchers_ids_from_request_body
from web.validate_exceptions import BadRequestPayload
from web.services.offer_watchers import get_user_watchers_grouped_by_city


class DoesNotHavePermissionsToForm(Exception):
    pass


class BaseOfferWatchersFormView(View):
    @staticmethod
    async def get_user_from_query_params(request):
        tg_user_id = request.GET.get('user_id')
        requested_user_session_id = request.GET.get('session_id')
        if not (tg_user_id and requested_user_session_id):
            raise DoesNotHavePermissionsToForm()

        cache_key_to_get_user_session_id = method_cache_key(
            value_is="session_id",
            user_telegram_id=tg_user_id
        )
        user_session_id = cache.get(cache_key_to_get_user_session_id)
        if str(user_session_id) != str(requested_user_session_id):
            raise DoesNotHavePermissionsToForm()

        try:
            user = await TelegramUser.objects.aget(telegram_id=tg_user_id)
        except ObjectDoesNotExist:
            raise DoesNotHavePermissionsToForm()

        return user

    @staticmethod
    def return_render_not_have_permissions(request) -> HttpResponse:
        return render(
            request,
            "errors/not_have_permissions.html",
            status=400
        )


class OfferWatchersCreateFormView(BaseOfferWatchersFormView):
    response_template = "offers_watchers_forms/offers_watchers_create_form.html"

    async def get(self, request) -> HttpResponse:
        try:
            user = await self.get_user_from_query_params(request=request)
        except DoesNotHavePermissionsToForm:
            return self.return_render_not_have_permissions(
                request=request
            )

        form = OfferWatchersForm(tg_user=user)
        return render(
            request,
            self.response_template,
            {"form": form, "car_models_by_brands": CAR_MODELS_BY_BRANDS}
        )

    async def post(self, request) -> HttpResponse:
        try:
            user = await self.get_user_from_query_params(request=request)
        except DoesNotHavePermissionsToForm:
            return self.return_render_not_have_permissions(
                request=request
            )

        form = OfferWatchersForm(request.POST, tg_user=user)
        if form.is_valid():
            await form.update_user_city_and_radius()
            await form.create_offer_watcher()
            delete_cache_stage_create_watcher(user.telegram_id)
            await bot.send_message(
                user.telegram_id, "Наблюдение создано ✅"
            )
            await send_menu_as_answer_on_message(telegram_user=user)

            return CustomSchemeRedirect(f"tg://resolve?domain=avito_offer_helper_bot")

        return render(
            request,
            self.response_template,
            {"form": form, "car_models_by_brands": CAR_MODELS_BY_BRANDS}
        )


class OfferWatchersEditFormView(BaseOfferWatchersFormView):
    response_template = "offers_watchers_forms/offers_watchers_edit_form.html"

    async def get(self, request) -> HttpResponse:
        try:
            user = await self.get_user_from_query_params(request=request)
        except DoesNotHavePermissionsToForm:
            return self.return_render_not_have_permissions(
                request=request
            )

        user_watchers_by_cities = await get_user_watchers_grouped_by_city(user_telegram_id=user.telegram_id)

        return render(
            request,
            self.response_template,
            {"user_watchers_by_cities": user_watchers_by_cities}
        )

    async def post(self, request) -> HttpResponse:
        try:
            user = await self.get_user_from_query_params(request=request)
        except DoesNotHavePermissionsToForm:
            return self.return_render_not_have_permissions(
                request=request
            )


        # form = OfferWatchersForm(request.POST, tg_user=user)
        # if form.is_valid():
        #     await form.update_user_city_and_radius()
        #     await form.create_offer_watcher()
        #     delete_cache_stage_create_watcher(user.telegram_id)
        #     await bot.send_message(
        #         user.telegram_id, "Наблюдение создано ✅"
        #     )
        #     await send_menu_as_answer_on_message(user_id=user.telegram_id)
        #
        #     return CustomSchemeRedirect(f"tg://resolve?domain=avito_offer_helper_bot")

        return render(
            request,
            self.response_template,
            # {"form": form, "car_models_by_brands": CAR_MODELS_BY_BRANDS}
        )

    async def delete(self, request) -> JsonResponse:
        RESPONSE_STATUS_KEY = "status"
        try:
            user = await self.get_user_from_query_params(request=request)
        except DoesNotHavePermissionsToForm:
            return JsonResponse({RESPONSE_STATUS_KEY: "No have permission"})

        try:
            request_watchers_ids_to_delete = parse_watchers_ids_from_request_body(request.body)
        except BadRequestPayload as e:
            return JsonResponse({RESPONSE_STATUS_KEY: e.response_message})

        user_watchers = AvitoUserOfferWatcher.objects.filter(
                telegram_user=user, id__in=request_watchers_ids_to_delete
            )
        count_found_user_offers_by_ids = await user_watchers.acount()
        if count_found_user_offers_by_ids != len(request_watchers_ids_to_delete):
            return JsonResponse({RESPONSE_STATUS_KEY: "Error, not found watchers"})

        await user_watchers.aupdate(is_deleted=True)

        user_watchers_by_cities = await get_user_watchers_grouped_by_city(user_telegram_id=user.telegram_id)
        return JsonResponse({RESPONSE_STATUS_KEY: "ok", "user_watchers_by_cities": user_watchers_by_cities})
