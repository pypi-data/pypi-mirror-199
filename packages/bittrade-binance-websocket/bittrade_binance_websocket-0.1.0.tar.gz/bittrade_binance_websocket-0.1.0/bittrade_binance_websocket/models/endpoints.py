from enum import Enum


class BinanceEndpoints(Enum):
    GET_TIME = "/api/v3/time"
    LISTEN_KEY = "/api/v3/userDataStream"
