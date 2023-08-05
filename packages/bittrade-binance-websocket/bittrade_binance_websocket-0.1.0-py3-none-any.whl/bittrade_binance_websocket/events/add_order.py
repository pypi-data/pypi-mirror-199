import dataclasses
from datetime import datetime
from logging import getLogger
import time
from typing import Callable, Dict, cast
from uuid import uuid4
from expression import pipe
from reactivex import Observable, compose, operators
from bittrade_binance_websocket.connection.sign import encode_query_string, get_signature, to_sorted_qs
from bittrade_binance_websocket.events.request_response import response_ok, wait_for_response
from bittrade_binance_websocket.models.enhanced_websocket import EnhancedWebsocket
from bittrade_binance_websocket.models.message import UserFeedMessage
from bittrade_binance_websocket.models.order import PlaceOrderRequest, PlaceOrderResponse
from bittrade_binance_websocket.models.private import PrivateRequest

from bittrade_binance_websocket.models.response_message import ResponseMessage

logger = getLogger(__name__)

@dataclasses.dataclass
class OrderRequest(PlaceOrderRequest, PrivateRequest):
   pass

def add_order(
    messages: Observable[ResponseMessage],
    request: PlaceOrderRequest
  ) -> Callable[[Observable[EnhancedWebsocket]], Observable[ResponseMessage]]:
  def socket_to_event_messages(
    socket: EnhancedWebsocket
  ) -> Observable[ResponseMessage]:
      request_id = str(uuid4())
      timestamp = str(int(datetime.now().timestamp()*1e3))

      sign = get_signature(socket.secret)
      request_dict = dataclasses.asdict(request)
      request_dict['apiKey'] = socket.key
      request_dict['timestamp'] = timestamp

      signature = pipe(request_dict, to_sorted_qs, encode_query_string, sign)
      order_params = OrderRequest(**request_dict, signature=signature)
      
      order_request = {
         'id': request_id,
         'method': 'order.place',
         'params': dataclasses.asdict(order_params)
      }
      logger.info(f'add order request, {order_request}')

      socket.send_message(order_request)
      return messages.pipe(
        wait_for_response(request_id, 5.0),
        response_ok(),
      )
  
  return compose(
    operators.flat_map(socket_to_event_messages)
  )