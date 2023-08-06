from logging import getLogger
from typing import TYPE_CHECKING, Any, Callable, Optional, cast

import requests
from ccxt import binance
from elm_framework_helpers.output import debug_operator
from elm_framework_helpers.websockets.operators import connection_operators
from reactivex import Observable, operators
from reactivex.disposable import CompositeDisposable
from reactivex.operators import flat_map, share
from reactivex.scheduler import ThreadPoolScheduler
from reactivex.subject import BehaviorSubject

from bittrade_binance_websocket import models
from bittrade_binance_websocket.connection.private import private_websocket_connection
from bittrade_binance_websocket.connection.private_user_stream import (
    private_websocket_user_stream,
)
from bittrade_binance_websocket.events.add_order import create_order_factory
from bittrade_binance_websocket.events.cancel_order import (
    cancel_order_factory,
    cancel_symbol_orders_factory,
)
from bittrade_binance_websocket.rest.symbol_orders_cancel import (
    delete_symbol_order_http_factory,
)
from bittrade_binance_websocket.rest.current_open_orders import (
    current_open_orders_http_factory,
)
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket
from bittrade_binance_websocket.models.framework import FrameworkContext
from bittrade_binance_websocket.models.order import (
    OrderCancelRequest,
    OrderResponseType,
    OrderSide,
    OrderTimeInForceType,
    OrderType,
    PlaceOrderRequest,
    PlaceOrderResponse,
    SymbolOrderResponseItem,
)
from bittrade_binance_websocket.rest.symbol_price_ticker import symbol_price_ticker_http
from bittrade_binance_websocket.rest.listen_key import (
    delete_listen_key_http_factory,
    get_active_listen_key_http_factory,
    get_listen_key_http_factory,
    ping_listen_key_http_factory,
)

logger = getLogger(__name__)


def get_framework(
    *,
    add_token: Callable[
        [Observable[models.ResponseMessage]],
        Callable[
            [Observable[models.EnhancedWebsocket]], Observable[models.ResponseMessage]
        ],
    ] = None,
    user_stream_signer_http: Callable[
        [requests.models.Request], requests.models.Request
    ] = None,
    spot_trade_signer: Callable[
        [models.EnhancedWebsocket], models.EnhancedWebsocket
    ] = None,
    spot_trade_signer_http: Callable[
        [requests.models.Request], requests.models.Request
    ] = None,
    load_markets=True,
) -> FrameworkContext:
    exchange = binance()
    if load_markets:
        exchange.load_markets()
    pool_scheduler = ThreadPoolScheduler(200)
    all_subscriptions = CompositeDisposable()
    # Rest
    get_active_listen_key_http = get_active_listen_key_http_factory(
        user_stream_signer_http
    )
    get_listen_key_http = get_listen_key_http_factory(user_stream_signer_http)
    keep_alive_listen_key_http = ping_listen_key_http_factory(user_stream_signer_http)
    delete_listen_key_http = delete_listen_key_http_factory(user_stream_signer_http)

    # Set up sockets
    user_data_stream_socket_bundles = private_websocket_user_stream(
        get_listen_key_http, keep_alive_listen_key_http
    )
    user_data_stream_socket = user_data_stream_socket_bundles.pipe(
        connection_operators.keep_new_socket_only()
    )

    user_data_stream_messages = user_data_stream_socket_bundles.pipe(
        connection_operators.keep_messages_only()
    )

    spot_trade_socket_bundles = private_websocket_connection()
    spot_trade_sockets = spot_trade_socket_bundles.pipe(
        connection_operators.keep_new_socket_only(),
        operators.map(spot_trade_signer),  # add authentication details
        operators.share(),
    )
    spot_trade_guaranteed_sockets: BehaviorSubject[EnhancedWebsocket] = BehaviorSubject(
        cast(EnhancedWebsocket, None)
    )
    spot_trade_sockets.subscribe(spot_trade_guaranteed_sockets)
    spot_trade_socket_messages = spot_trade_socket_bundles.pipe(
        connection_operators.keep_messages_only(), operators.share()
    )
    spot_order_create = create_order_factory(
        spot_trade_guaranteed_sockets, spot_trade_socket_messages
    )
    spot_order_cancel = cancel_order_factory(
        spot_trade_guaranteed_sockets, spot_trade_socket_messages
    )
    spot_symbol_orders_cancel = cancel_symbol_orders_factory(
        spot_trade_guaranteed_sockets, spot_trade_socket_messages
    )
    spot_symbol_orders_cancel_http = delete_symbol_order_http_factory(
        spot_trade_signer_http
    )
    spot_current_open_orders_http = current_open_orders_http_factory(
        spot_trade_signer_http
    )

    return FrameworkContext(
        all_subscriptions=all_subscriptions,
        exchange=exchange,
        delete_listen_key_http=delete_listen_key_http,
        get_active_listen_key_http=get_active_listen_key_http,
        get_listen_key_http=get_listen_key_http,
        keep_alive_listen_key_http=keep_alive_listen_key_http,
        market_symbol_price_ticker_http=symbol_price_ticker_http,
        spot_trade_socket_bundles=spot_trade_socket_bundles,
        spot_trade_socket_messages=spot_trade_socket_messages,
        spot_trade_sockets=spot_trade_sockets,
        spot_trade_guaranteed_sockets=spot_trade_guaranteed_sockets,
        spot_order_create=spot_order_create,
        spot_order_cancel=spot_order_cancel,
        spot_symbol_orders_cancel=spot_symbol_orders_cancel,
        spot_symbol_orders_cancel_http=spot_symbol_orders_cancel_http,
        spot_current_open_orders_http=spot_current_open_orders_http,
        user_data_stream_messages=user_data_stream_messages,
        user_data_stream_sockets=user_data_stream_socket,
        user_data_stream_socket_bundles=user_data_stream_socket_bundles,
        scheduler=pool_scheduler,
    )
