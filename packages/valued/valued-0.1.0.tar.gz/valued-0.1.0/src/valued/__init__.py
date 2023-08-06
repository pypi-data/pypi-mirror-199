from importlib.metadata import version

__version__ = version(__name__)

import concurrent.futures
import json
import logging
import typing
import datetime

import requests

__VALUED_VERSION__ = "0.0.1"


class Connection(object):
    DEFAULT_ENDPOINT = "https://ingest.valued.app/events"

    def __del__(self):
        self._pool.shutdown()

    def __init__(
        self, token: typing.AnyStr, endpoint: typing.AnyStr = DEFAULT_ENDPOINT
    ):
        self._pool = concurrent.futures.ThreadPoolExecutor()
        self._token = token
        self._endpoint = endpoint

    @property
    def endpoint(self) -> typing.AnyStr:
        return self._endpoint

    @property
    def token(self) -> typing.AnyStr:
        return self._token

    @property
    def headers(self) -> typing.Dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": f"valued-client/{__VALUED_VERSION__} (Python/{__version__})",
        }

    @staticmethod
    def call(
        endpoint: typing.AnyStr, headers: typing.Dict, data: typing.Dict
    ) -> typing.Optional[requests.Response]:
        try:
            resp = requests.post(
                endpoint,
                data=json.dumps(data),
                headers=headers,
                timeout=1,
            )
            logging.debug(resp.json())
        except Exception as e:
            logging.error("Exception sending data to ingestion point", exc_info=e)
        return resp

    def send(self, data):
        return self._pool.submit(self.call, self.endpoint, self.headers, data)


class Client(object):
    def __init__(self, *args, **kwargs):
        self._connection = Connection(*args, **kwargs)

    def action(self, key, data):
        data["key"] = key
        return self.send_event("action", data)

    def sync(self, data):
        return self.send_event("sync", data)

    def sync_customer(self, data):
        return self.sync({"customer": data})

    def sync_user(self, data):
        return self.sync({"user": data})

    def send_event(self, category: typing.AnyStr, data: typing.Dict):
        # TODO: Validate
        data["category"] = category
        if "occured_at" not in data.keys():
            data["occured_at"] = datetime.datetime.now().isoformat()
        return self._connection.send(data)
