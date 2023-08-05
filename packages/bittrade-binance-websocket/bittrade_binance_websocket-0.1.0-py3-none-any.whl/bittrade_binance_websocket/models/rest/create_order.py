import dataclasses
from decimal import Decimal
from typing import Any, Literal, Optional
from ccxt import huobi

OrderType = Literal[
    "LIMIT",
    "MARKET",
    "STOP_LOSS",
    "STOP_LOSS_LIMIT",
    "TAKE_PROFIT",
    "TAKE_PROFIT_LIMIT",
    "LIMIT_MAKER",
]


@dataclasses.dataclass
class OrderCreateParams:
    account_id: str
    amount: str
    price: str
    symbol: str
    type: OrderType
    source: str = "spot-api"
    client_order_id: str = ""
    stop_price: str = ""

    def to_dict(self):
        as_dict = dataclasses.asdict(self)
        del as_dict["account_id"]
        as_dict["account-id"] = self.account_id
        del as_dict["client_order_id"]
        if self.client_order_id:
            as_dict["client-order-id"] = self.client_order_id
        del as_dict["stop_price"]
        if self.stop_price:
            as_dict["stop-price"] = self.stop_price
        as_dict["source"] = "api"
        return as_dict


@dataclasses.dataclass
class OrderCreateResponse:
    status: str
    data: str
