from logging import getLogger
import os
from typing import Any, Optional

from reactivex import ConnectableObservable
from reactivex.abc import SchedulerBase
from reactivex.operators import publish

from bittrade_binance_websocket.connection.reconnect import retry_with_backoff
from bittrade_binance_websocket.connection.generic import raw_websocket_connection

logger = getLogger(__name__)

USER_URL = os.getenv('BINANCE_USER_WEBSOCKET', 'wss://stream.binance.com:9443/ws')


def private_websocket_user_stream(
    *, listen_key: str, reconnect: bool = True, scheduler: Optional[SchedulerBase] = None,
) -> ConnectableObservable[Any]:
    url = f'{USER_URL}/{listen_key}'
    connection = raw_websocket_connection(url=url, scheduler=scheduler)
    if reconnect:
        connection = connection.pipe(retry_with_backoff())

    return connection.pipe(publish())


__all__ = [
    "private_websocket_user_stream",
]
