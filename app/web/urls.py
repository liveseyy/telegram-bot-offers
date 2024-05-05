from django.urls import path
from django.conf import settings
from web.views import OfferWatchersCreateFormView, OfferWatchersEditFormView


urlpatterns = [
    path(f'{settings.OFFERS_CAR_WATCHER_FORM_CREATE_URL_PREFIX}/', OfferWatchersCreateFormView.as_view()),
    path(f'{settings.OFFERS_CAR_WATCHER_FORM_EDIT_URL_PREFIX}/', OfferWatchersEditFormView.as_view()),
]
