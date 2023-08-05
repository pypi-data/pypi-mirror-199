from dataclasses import dataclass
from typing import Any, Callable, Literal, NamedTuple, Optional

from ccxt import binance
from elm_framework_helpers.ccxt.models.orderbook import Orderbook
from reactivex import Observable
from reactivex.observable import ConnectableObservable
from reactivex.disposable import CompositeDisposable
from reactivex.scheduler import ThreadPoolScheduler
from elm_framework_helpers.websockets import models
from bittrade_binance_websocket.models.rest import market_depth, get_all_open_orders
from bittrade_binance_websocket.models import UserFeedMessage, HttpResponse

from bittrade_binance_websocket.models.rest.cancel_orders_batch import (
    CancelOrdersBatchData,
    CancelOrdersBatchParams,
)
from bittrade_binance_websocket.models.rest.create_order import (
    OrderCreateParams,
    OrderCreateResponse,
)


class BookConfig(NamedTuple):
    pair: str
    depth: int


@dataclass
class FrameworkContext:
    all_subscriptions: CompositeDisposable
    authenticated_sockets: Observable[models.EnhancedWebsocket]
    books: dict[str, Observable[Orderbook]]
    exchange: binance
    public_socket_connection: ConnectableObservable[models.WebsocketBundle]
    private_socket_connection: ConnectableObservable[models.WebsocketBundle]
    private_messages: Observable[UserFeedMessage]
    scheduler: ThreadPoolScheduler
    websocket_bs: models.EnhancedWebsocketBehaviorSubject
    open_orders_http: Callable[
        [get_all_open_orders.AllOpenOrdersParams],
        Observable[get_all_open_orders.AllOpenOrdersResponse],
    ]
