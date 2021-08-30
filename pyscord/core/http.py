# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pyscord
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
from enum import Enum
from typing import Dict, Any, Protocol

from aiohttp import ClientSession
from aiohttp.client import _RequestContextManager
from aiohttp.typedefs import StrOrURL

from ..exceptions import NotFoundError, BadRequestError, NotModifiedError, \
    UnauthorizedError, ForbiddenError, MethodNotAllowedError, RateLimitError, \
    ServerError, HTTPError


class RequestMethod(Enum):
    GET = 0
    POST = 1
    DELETE = 2
    PUT = 3
    OPTIONS = 4


class HttpCallable(Protocol):
    def __call__(self, url: StrOrURL, *, allow_redirects: bool = True,
                 **kwargs: Any) -> "_RequestContextManager":
        ...


class HTTPClient:
    def __init__(self, token: str, version: int = 9, ttl: int = 4):
        """
        Instantiate a new HttpApi object.

        :param token: Discord API token

        Keyword Arguments:
        :param version: The discord API version.
                        See https://discord.com/developers/docs/reference#api-versioning.
        :param ttl: Max amount of attempts after
                            error code 5xx
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
            439: RateLimitError()
        }

    async def __send(self, method: RequestMethod, route: str, *,
                     __ttl: int = None):
        # TODO: Fix docs
        # TODO: Implement logging
        __ttl = self.max_ttl if __ttl is None else __ttl

        if __ttl == 0:
            raise ServerError(f"Maximum amount of retries for `{route}`.")

        async with ClientSession() as session:
            methods: Dict[RequestMethod, HttpCallable] = {
                RequestMethod.GET: session.get,
                RequestMethod.POST: session.post,
                RequestMethod.DELETE: session.delete,
                RequestMethod.PUT: session.put,
                RequestMethod.OPTIONS: session.options
            }

            sender = methods.get(method)

            if not sender:
                raise RuntimeError("Invalid RequestMethod has been passed.")

            async with sender(f"{self.endpoint}/{route}",
                              headers=self.header) as res:

                if res.status in [200, 201, 204]:
                    return await res.json()

                exception = self.__http_exceptions.get(res.status)

                if exception:
                    exception.__init__(res.reason)
                    raise exception
                elif res.status == 502:
                    await asyncio.sleep(3)
                    await self.__send(method, route, __ttl=__ttl - 1)

    async def get(self, route: str) -> Dict:
        """
        :return: JSON response from the discord API.
        """
        return await self.__send(RequestMethod.GET, route)
