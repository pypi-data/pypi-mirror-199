from os import getenv
import os
from typing import Literal
import requests
import reactivex
from reactivex.disposable import Disposable
from logging import getLogger
from bittrade_binance_websocket import models

MARKET_URL = getenv("BINANCE_HTTP_MARKET_URL", "https://api.binance.com")

session = requests.Session()

logger = getLogger(__name__)


def generate_add_api_key(api_key: str = ''):
    key = os.getenv('BINANCE_API_KEY', api_key)

    def _add_api_key(request: requests.models.Request):
        request.headers.update({
            'X-MBX-APIKEY': key
        })
        logger.info(request.headers)
        return request

    return _add_api_key

def prepare_request(message: models.RequestMessage) -> requests.models.Request:
    http_method = message.method
    kwargs = {}
    # check if message params are set, if not, ignores
    if message.params:
        if http_method == "GET":
            kwargs["params"] = message.params
        else:
            kwargs["data"] = message.params

    # There are (few) cases where the endpoint must be a string; "handle" that below
    try:
        endpoint = message.endpoint.value
    except:
        endpoint = message.endpoint
    return requests.Request(http_method, f"{MARKET_URL}{endpoint}", **kwargs)


def send_request(request: requests.models.Request) -> reactivex.Observable:
    def subscribe(
        observer: reactivex.abc.ObserverBase,
        scheduler: reactivex.abc.SchedulerBase | None = None,
    ) -> reactivex.abc.DisposableBase:
        response = session.send(request.prepare())
        if response.ok:
            try:
                body = response.json()
                observer.on_next(body)
                observer.on_completed()
            except Exception as exc:
                logger.error(
                    "Error parsing request %s; request was %s",
                    response.text,
                    response.request.body
                    if request.method == "POST"
                    else response.request.headers,
                )
                observer.on_error(exc)
        else:
            try:
                logger.error(
                    "Error with request %s; request was %s",
                    response.text,
                    response.request.body
                    if request.method == "POST"
                    else response.request.headers,
                )
                response.raise_for_status()
            except Exception as exc:
                observer.on_error(exc)
        return Disposable()

    return reactivex.Observable(subscribe)
