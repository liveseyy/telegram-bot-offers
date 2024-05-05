import json

from common.utils import iterable_has_only_digits
from web.validate_exceptions import BadRequestPayload


def parse_watchers_ids_from_request_body(request_body: bytes) -> list:
    try:
        request_watchers_ids_to_delete = json.loads(request_body)["watchersIdsToDelete"]
    except json.decoder.JSONDecodeError:
        raise BadRequestPayload(response_message="Bad format")
    except (KeyError, TypeError):
        raise BadRequestPayload(response_message="Need object with 'watchersToDelete'")

    if not isinstance(request_watchers_ids_to_delete, list):
        raise BadRequestPayload(response_message="watchersToDelete must be array")

    if not iterable_has_only_digits(request_watchers_ids_to_delete):
        raise BadRequestPayload(response_message="watcherIds must be integers")

    return request_watchers_ids_to_delete
