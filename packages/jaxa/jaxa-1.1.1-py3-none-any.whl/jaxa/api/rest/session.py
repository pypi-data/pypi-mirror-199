"""Base session"""

import logging
import time
from datetime import datetime
from enum import Enum
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Optional, Union

import requests

logger = logging.getLogger(__package__)

RATE_LIMIT_STATUS_CODE = 429


class HTTPMethods(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"


class APIError(Exception):
    """Base Exception"""


class StatusCodeError(APIError):
    """Status code Exception"""


class RESTSession:
    """Base Session for making REST calls"""

    _user_agent = "Python JAXA"

    def __init__(
        self,
        url: Optional[str] = None,
        exc: bool = False,
        rate_limit: bool = True,
        **kwargs,
    ) -> None:
        """
        :param url:
            Base address
        :param exc:
            Catching exceptions
        :param kwargs:
            :key timeout: int (default: 30)
                How many seconds to wait for the server to send data
            :key verify: bool (default: True)
                Controls whether we verify the server's certificate
            :key headers: dict
                Dictionary of HTTP Headers to send
            :key retry: int (default 3)
                Delay in receiving code 429
            :key exc_iterations: int (default 3)
        """
        self.__base_url = url.rstrip("/")
        self.__timeout = kwargs.get("timeout", 30)
        self.__session = requests.Session()
        self.__session.headers["User-Agent"] = self._user_agent
        self.__session.headers.update(kwargs.get("headers", {}))
        self.__session.verify = kwargs.get("verify", True)
        self.__retry = kwargs.get("retry", 3)
        self.__session.auth = None
        self.__exc = exc
        self.__exc_iterations = kwargs.get("exc_iterations", 3)
        self._rate_limit = rate_limit
        logger.debug(
            "Create Session{url: %s, timeout: %s, headers: %s, verify: "
            "%s, exception: %s, exc_iterations: %s, retry: %s}",
            url,
            self.__timeout,
            self.__session.headers,
            self.__session.verify,
            self.__exc,
            self.__exc_iterations,
            self.__retry,
        )

    def set_basic_auth(self, username, password):
        self.__session.auth = (username, password)

    def __response(self, response: requests.Response):
        if not response.ok:
            logger.error(
                "Code: %s, reason: %s url: %s, content: %s",
                response.status_code,
                response.reason,
                response.url,
                response.content,
            )
            if not self.__exc:
                raise StatusCodeError(
                    response.status_code,
                    response.reason,
                    response.url,
                    response.content,
                )

        # logger.debug("Response body: %s", response.text)
        try:
            return response.json()
        except (JSONDecodeError, ValueError):
            return response.text or None

    @staticmethod
    def __get_converter(params: dict) -> None:
        """Converting GET parameters"""
        for key, value in params.items():
            if isinstance(value, (list, tuple, set)):
                # Converting a list to a string '1,2,3'
                params[key] = ",".join(str(i) for i in value)
            elif isinstance(value, bool):
                # Converting a boolean value to integer
                params[key] = int(value)
            elif isinstance(value, datetime):
                # Converting a datetime value to integer (UNIX timestamp)
                params[key] = round(value.timestamp())

    @staticmethod
    def __post_converter(json: dict) -> None:
        """Converting POST parameters"""
        for key, value in json.items():
            if isinstance(value, datetime):
                # Converting a datetime value to integer (UNIX timestamp)
                json[key] = round(value.timestamp())

    def request(self, method: HTTPMethods, endpoint: str, raw: bool = False, **kwargs):
        """Base request method"""
        url = f"{self.__base_url}/{endpoint}"

        self.__get_converter(kwargs.get("params", {}))
        self.__post_converter(kwargs.get("json", {}))

        for count in range(self.__exc_iterations):
            try:
                response = self.__session.request(
                    method=method.value, url=url, timeout=self.__timeout, **kwargs
                )
            except Exception as err:
                logger.error("%s", err, exc_info=True)
                raise
            if (
                self._rate_limit
                and response.status_code == RATE_LIMIT_STATUS_CODE
                and count < self.__exc_iterations - 1
            ):
                time.sleep(int(response.headers.get("retry-after", self.__retry)))
                continue
            return response if raw else self.__response(response)

    def get(self, endpoint: str, raw: bool = False, **kwargs):
        return self.request(
            method=HTTPMethods.GET, endpoint=endpoint, raw=raw, **kwargs
        )

    def post(self, endpoint: str, raw: bool = False, **kwargs):
        return self.request(
            method=HTTPMethods.POST, endpoint=endpoint, raw=raw, **kwargs
        )

    def put(self, endpoint: str, raw: bool = False, **kwargs):
        return self.request(
            method=HTTPMethods.PUT, endpoint=endpoint, raw=raw, **kwargs
        )

    @staticmethod
    def _path(path: Union[Path, str]) -> Path:
        return path if isinstance(path, Path) else Path(path)
