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
from enum import Enum, auto
from json import dumps
from typing import Dict, Any, Optional, Protocol

from aiohttp import ClientSession
from aiohttp.client import _RequestContextManager
from aiohttp.typedefs import StrOrURL

from pincer import __package__
from pincer.exceptions import (
    NotFoundError, BadRequestError, NotModifiedError, UnauthorizedError,
    ForbiddenError, MethodNotAllowedError, RateLimitError, ServerError,
    HTTPError
)

log = logging.getLogger(__package__)


class RequestMethod(Enum):
    """HTTP Protocols supported by aiohttp"""

    DELETE = auto()
    GET = auto()
    HEAD = auto()
    OPTIONS = auto()
    PATCH = auto()
    POST = auto()
    PUT = auto()


class HttpCallable(Protocol):
    """aiohttp HTTP method"""

    def __call__(
        self, url: StrOrURL, *,
        allow_redirects: bool = True, json: Dict = None, **kwargs: Any
    ) -> _RequestContextManager:
        pass


class HTTPClient:
    """Interacts with Discord API through HTTP protocol"""

    def __init__(self, token: str, version: int = 9, ttl: int = 5):
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
        self.header: Dict[str, str] = {
            "Authorization": f"Bot {token}"
        }
        self.endpoint: str = f"https://discord.com/api/v{version}"
        self.max_ttl: int = ttl
        self.__http_exceptions: Dict[int, HTTPError] = {
            304: NotModifiedError(),
            400: BadRequestError(),
            401: UnauthorizedError(),
            403: ForbiddenError(),
            404: NotFoundError(),
            405: MethodNotAllowedError(),
            429: RateLimitError()
        }

    async def __send(
        self, method: RequestMethod, endpoint: str, *,
        __ttl: int = None, data: Optional[Dict] = None
    ) -> Dict:
        """
        Send an api request to the Discord REST API.

        :param method: The method for the request. (eg GET or POST)
        :param endpoint: The endpoint to which the request will be sent.
        :param __ttl: Private param used for recursively setting the
        retry amount. (Eg set to 1 for 1 max retry)
        :param data: The data which will be added to the request.
        """
        __ttl = __ttl or self.max_ttl

        if __ttl == 0:
            logging.error(
                f"{method.name} {endpoint} has reached the "
                f"maximum retry count of  {self.max_ttl}."
            )

            raise ServerError(f"Maximum amount of retries for `{endpoint}`.")

        async with ClientSession() as session:
            methods: Dict[RequestMethod, HttpCallable] = {
                RequestMethod.DELETE: session.delete,
                RequestMethod.GET: session.get,
                RequestMethod.HEAD: session.head,
                RequestMethod.OPTIONS: session.options,
                RequestMethod.PATCH: session.patch,
                RequestMethod.POST: session.post,
                RequestMethod.PUT: session.put,
            }

            sender = methods.get(method)

            if not sender:
                log.debug(
                    "Could not find provided RequestMethod "
                    f"({method.name}) key in `methods` "
                    f"[http.py>__send]."
                )

                raise RuntimeError("Unsupported RequestMethod has been passed.")

            log.debug(f"new {method.name} {endpoint} | {dumps(data)}")

            async with sender(
                f"{self.endpoint}/{endpoint}",
                headers=self.header, json=data
            ) as res:
                if res.ok:
                    log.debug(
                        "Request has been sent successfully. "
                        "Returning json response."
                    )

                    return (
                        await res.json()
                        if res.content_type == "application/json"
                        else {}
                    )

                exception = self.__http_exceptions.get(res.status)

                if exception:
                    log.error(
                        f"An http exception occurred while trying to send "
                        f"a request to {endpoint}. ({res.status}, {res.reason})"
                    )

                    exception.__init__(res.reason)
                    raise exception

                # status code is guaranteed to be 5xx
                retry_in = 1 + (self.max_ttl - __ttl) * 2
                log.debug(
                    "Server side error occurred with status code "
                    f"{res.status}. Retrying in {retry_in}s."
                )

                await asyncio.sleep(retry_in)
                await self.__send(method, endpoint, __ttl=__ttl - 1, data=data)

    async def delete(self, route: str) -> Dict:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(RequestMethod.DELETE, route)

    async def get(self, route: str) -> Dict:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(RequestMethod.GET, route)

    async def head(self, route: str) -> Dict:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(RequestMethod.HEAD, route)

    async def options(self, route: str) -> Dict:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(RequestMethod.OPTIONS, route)

    async def patch(self, route: str, data: Dict) -> Dict:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(RequestMethod.PATCH, route, data=data)

    async def post(self, route: str, data: Dict) -> Dict:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(RequestMethod.POST, route, data=data)

    async def put(self, route: str, data: Dict) -> Dict:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(RequestMethod.PUT, route, data=data)
