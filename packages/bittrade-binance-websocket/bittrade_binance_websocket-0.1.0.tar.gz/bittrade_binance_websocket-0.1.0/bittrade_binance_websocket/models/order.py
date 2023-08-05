import dataclasses
from enum import Enum
from typing import Optional

class OrderSide(Enum):
  BUY = 'BUY'
  SELL = 'SELL'

class OrderType(Enum):
  LIMIT = 'LIMIT'
  LIMIT_MAKER = 'LIMIT_MAKER'
  MARKET = 'MARKET'
  STOP_LOSS = 'STOP_LOSS'
  STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
  TAKE_PROFIT = 'TAKE_PROFIT'
  TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'

class OrderTimeInForceType(Enum):
  GTC = 'GTC'	# Good 'til Canceled – the order will remain on the book until you cancel it, or the order is completely filled.
  IOC = 'IOC'	# Immediate or Cancel – the order will be filled for as much as possible, the unfilled quantity immediately expires.
  FOK = 'FOK'	# Fill or Kill – the order will expire unless it cannot be immediately filled for the entire quantity.

class OrderResponseType(Enum):
  ACK = 'ACK'
  RESULT = 'RESULT'
  FULL = 'FULL'

class OrderSelfTradePreventionMode(Enum):
  EXPIRE_TAKER = 'EXPIRE_TAKER'
  EXPIRE_MAKER = 'EXPIRE_MAKER'
  EXPIRE_BOTH = 'EXPIRE_BOTH'
  NONE = 'NONE'

class OrderCancelRestrictions(Enum):
  ONLY_NEW = 'ONLY_NEW'
  ONLY_PARTIALLY_FILLED = 'ONLY_PARTIALLY_FILLED'

'''
Optional without default value is dependant on order type. Set "None" for those that are not related
'''
@dataclasses.dataclass
class PlaceOrderRequest:
  symbol: str
  side: OrderSide
  type: OrderType
  timeInForce: Optional[OrderTimeInForceType]
  price: Optional[float]
  quantity: Optional[float]
  quoteOrderQty: Optional[float]
  stopPrice: Optional[float]
  trailingDelta: Optional[int]
  icebergQty: Optional[float] = None
  strategyId: Optional[int] = None
  strategyType: Optional[int] = None
  selfTradePreventionMode: Optional[OrderSelfTradePreventionMode] = None
  newOrderRespType: Optional[OrderResponseType] = None
  newClientOrderId: Optional[str] = None # Arbitrary unique ID among open orders. Automatically generated if not sent
  recvWindow: Optional[int] = None
  
@dataclasses.dataclass
class PlaceOrderResponse:
  symbol: str
  orderId: int
  orderListId: int
  clientOrderId: str
  transactTime: int

@dataclasses.dataclass
class OrderCancelRequest:
  symbol: str
  origClientOrderId: Optional[str]
  orderId: Optional[int]
  newClientOrderId: Optional[str] = None
  cancelRestrictions: Optional[OrderCancelRestrictions] = None
  recvWindow: Optional[int] = None