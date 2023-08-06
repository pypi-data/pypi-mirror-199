from typing import Any, Callable

from reactivex import Observable, just, throw
from reactivex import operators
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import order

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(list[order.SymbolOrderResponseItem])
def current_open_orders_http_factory(params: order.SymbolOrdersCancelRequest):
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.CURRENT_OPEN_ORDERS,
        params={"symbol": params.symbol, "recvWindow": params.recvWindow},
    )
