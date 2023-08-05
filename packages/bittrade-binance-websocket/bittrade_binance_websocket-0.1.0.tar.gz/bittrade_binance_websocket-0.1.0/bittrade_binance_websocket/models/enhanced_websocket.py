from typing import Any
from elm_framework_helpers.websockets import models
import orjson


def del_none(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    # For Python 3, write `list(d.items())`; `d.items()` won’t work
    # For Python 2, write `d.items()`; `d.iteritems()` won’t work
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

class EnhancedWebsocket(models.EnhancedWebsocket):
    secret: str
    key: str

    def send_message(self, message: Any) -> int | str:
        return self.send_json(message)

    def prepare_request(self, message: Any) -> tuple[str, bytes]:
        self._id += 1
        # for binance, market stream and websocket api needs to have id
        if type(message) is dict and not message['id']:
            message['id'] = self._id

        if getattr(message, 'copy', None):
            message = del_none(message.copy())

        return f"id{self._id}", orjson.dumps(message)
