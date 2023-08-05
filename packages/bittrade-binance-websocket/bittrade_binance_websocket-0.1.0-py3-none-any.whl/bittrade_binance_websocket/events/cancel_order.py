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
from bittrade_binance_websocket.models.order import OrderCancelRequest, PlaceOrderRequest, PlaceOrderResponse
from bittrade_binance_websocket.models.private import PrivateRequest

from bittrade_binance_websocket.models.response_message import ResponseMessage

logger = getLogger(__name__)

@dataclasses.dataclass
class CancelOrderRequest(OrderCancelRequest, PrivateRequest):
   pass

def cancel_order(
    messages: Observable[ResponseMessage],
    request: OrderCancelRequest
  ) -> Callable[[Observable[EnhancedWebsocket]], Observable[ResponseMessage]]:
  def socket_to_event_messages(
    socket: EnhancedWebsocket
  ) -> Observable[ResponseMessage]:
      request_id = str(uuid4())
      timestamp = str(int(datetime.now().timestamp()*1e3))

      # do not allow for both to be None
      if not request.orderId and not request.origClientOrderId:
         raise Exception('cancel order request requires orderId or origClientOrderId to be filled.')

      sign = get_signature(socket.secret)
      request_dict = dataclasses.asdict(request)
      request_dict['apiKey'] = socket.key
      request_dict['timestamp'] = timestamp

      signature = pipe(request_dict, to_sorted_qs, encode_query_string, sign)
      order_params = CancelOrderRequest(**request_dict, signature=signature)
      
      order_request = {
         'id': request_id,
         'method': 'order.cancel',
         'params': dataclasses.asdict(order_params)
      }
      logger.info(f'cancel order request, {order_request}')

      socket.send_message(order_request)
      return messages.pipe(
        wait_for_response(request_id, 5.0),
        response_ok(),
      )
  
  return compose(
    operators.flat_map(socket_to_event_messages)
  )