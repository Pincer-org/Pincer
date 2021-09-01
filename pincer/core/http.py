# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import asyncio
import logging
from json import dumps
from typing import Dict, Any, Optional, Protocol

from aiohttp import ClientSession, ClientResponse
from aiohttp.client import _RequestContextManager
from aiohttp.typedefs import StrOrURL

from pincer import __package__
from pincer.exceptions import (
    NotFoundError, BadRequestError, NotModifiedError, UnauthorizedError,
    ForbiddenError, MethodNotAllowedError, RateLimitError, ServerError,
    HTTPError
)

_log = logging.getLogger(__package__)


class HttpCallable(Protocol):
    """aiohttp HTTP method"""

    def __call__(
            self, url: StrOrURL, *,
            allow_redirects: bool = True, json: Dict = None, **kwargs: Any
    ) -> _RequestContextManager:
        pass


class HTTPClient:
    """Interacts with Discord API through HTTP protocol"""

    def __init__(self, token: str, *, version: int, ttl: int = 5):
        """
        Instantiate a new HttpApi object.

        :param token:
            Discord API token

        Keyword Arguments:

        :param version:
            The discord API version.
            See `developers/docs/reference#api-versioning`.

        :param ttl:
            Max amount of attempts after error code 5xx
        """
        self.url: str = f"https://discord.com/api/v{version}"
        self.max_ttl: int = ttl

        headers: Dict[str, str] = {
            "Authorization": f"Bot {token}"
        }
        self.__session = ClientSession(headers=headers)

        self.__http_exceptions: Dict[int, HTTPError] = {
            304: NotModifiedError(),
            400: BadRequestError(),
            401: UnauthorizedError(),
            403: ForbiddenError(),
            404: NotFoundError(),
            405: MethodNotAllowedError(),
            429: RateLimitError()
        }

    # for with block
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        await self.__session.close()

    async def __send(
            self, method: HttpCallable, endpoint: str, *,
            data: Optional[Dict] = None, __ttl: int = None
    ) -> Optional[Dict]:
        """
        Send an api request to the Discord REST API.

        :param method: The method for the request. (eg GET or POST)
        :param endpoint: The endpoint to which the request will be sent.
        :param __ttl: Private param used for recursively setting the
        retry amount. (Eg set to 1 for 1 max retry)
        :param data: The data which will be added to the request.
        """
        ttl = __ttl or self.max_ttl

        if ttl == 0:
            logging.error(
                # TODO: print better method name
                f"{method.__name__.upper()} {endpoint} has reached the "
                f"maximum retry count of {self.max_ttl}."
            )

            raise ServerError(f"Maximum amount of retries for `{endpoint}`.")

        # TODO: print better method name
        _log.debug(f"{method.__name__.upper()} {endpoint} | {dumps(data)}")

        url = f"{self.url}/{endpoint}"
        async with method(url, json=data) as res:
            return await self.__handle_response(
                res, method, endpoint, ttl, data
            )

    async def __handle_response(
            self,
            res: ClientResponse,
            method: HttpCallable,
            endpoint: str,
            __ttl: int,
            data: Optional[Dict],
    ) -> Optional[Dict]:
        """Handle responses from the discord API."""
        if res.ok:

            if res.status == 204:
                _log.debug(
                    "Request has been sent successfully. "
                )
                return

            _log.debug(
                "Request has been sent successfully. "
                "Returning json response."
            )

            return await res.json()

        exception = self.__http_exceptions.get(res.status)

        if exception:
            _log.error(
                f"An http exception occurred while trying to send "
                f"a request to {endpoint}. ({res.status}, {res.reason})"
            )

            exception.__init__(res.reason)
            raise exception

        # status code is guaranteed to be 5xx
        retry_in = 1 + (self.max_ttl - __ttl) * 2

        _log.debug(
            "Server side error occurred with status code "
            f"{res.status}. Retrying in {retry_in}s."
        )

        await asyncio.sleep(retry_in)

        # try sending it again
        return await self.__send(method, endpoint, __ttl=__ttl - 1, data=data)

    async def delete(self, route: str) -> Optional[Dict]:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(self.__session.delete, route)

    async def get(self, route: str) -> Optional[Dict]:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(self.__session.get, route)

    async def head(self, route: str) -> Optional[Dict]:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(self.__session.head, route)

    async def options(self, route: str) -> Optional[Dict]:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(self.__session.options, route)

    async def patch(self, route: str, data: Dict) -> Optional[Dict]:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(self.__session.patch, route, data=data)

    async def post(self, route: str, data: Dict) -> Optional[Dict]:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(self.__session.post, route, data=data)

    async def put(self, route: str, data: Dict) -> Optional[Dict]:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(self.__session.put, route, data=data)
