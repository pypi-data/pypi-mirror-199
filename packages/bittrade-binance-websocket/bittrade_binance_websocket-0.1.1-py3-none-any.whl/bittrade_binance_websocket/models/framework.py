from dataclasses import dataclass
from typing import Any, Callable, Literal, NamedTuple, Optional

from ccxt import binance
from elm_framework_helpers.ccxt.models.orderbook import Orderbook
from reactivex import Observable
from reactivex.observable import ConnectableObservable
from reactivex.disposable import CompositeDisposable
from reactivex.scheduler import ThreadPoolScheduler
from elm_framework_helpers.websockets import models
from bittrade_binance_websocket.events.cancel_order import CancelOrderRequest
from bittrade_binance_websocket.models import UserFeedMessage
from bittrade_binance_websocket.models.response_message import SpotResponseMessage
from bittrade_binance_websocket.models.rest.listen_key import CreateListenKeyResponse
from bittrade_binance_websocket.models.rest.symbol_price_ticker import SymbolPriceTicker
from bittrade_binance_websocket.models.order import (
    OrderCancelRequest,
    SymbolOrdersCancelRequest,
    PlaceOrderRequest,
    PlaceOrderResponse,
)


class BookConfig(NamedTuple):
    pair: str
    depth: int


@dataclass
class FrameworkContext:
    all_subscriptions: CompositeDisposable
    exchange: binance
    get_active_listen_key_http: Callable[[], Observable[CreateListenKeyResponse]]
    get_listen_key_http: Callable[[], Observable[CreateListenKeyResponse]]
    delete_listen_key_http: Callable[[str], Observable[None]]
    keep_alive_listen_key_http: Callable[[str], Observable[None]]
    market_symbol_price_ticker_http: Callable[[str], Observable[SymbolPriceTicker]]
    scheduler: ThreadPoolScheduler
    spot_trade_socket_bundles: ConnectableObservable[models.WebsocketBundle]
    spot_trade_socket_messages: Observable[dict]
    spot_trade_sockets: Observable[models.EnhancedWebsocket]
    spot_trade_guaranteed_sockets: models.EnhancedWebsocketBehaviorSubject
    spot_order_create: Callable[[PlaceOrderRequest], Observable[PlaceOrderResponse]]
    spot_order_cancel: Callable[[OrderCancelRequest], Observable[dict]]
    spot_symbol_orders_cancel: Callable[
        [SymbolOrdersCancelRequest], Observable[SpotResponseMessage]
    ]
    spot_symbol_orders_cancel_http: Callable[
        [SymbolOrdersCancelRequest], Observable[SpotResponseMessage]
    ]
    spot_current_open_orders_http: Callable[
        [SymbolOrdersCancelRequest], Observable[SpotResponseMessage]
    ]
    user_data_stream_sockets: Observable[models.EnhancedWebsocket]
    user_data_stream_socket_bundles: ConnectableObservable[models.WebsocketBundle]
    user_data_stream_messages: Observable[UserFeedMessage]
