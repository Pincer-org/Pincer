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

from typing import Dict, Union
import asyncio

import aiohttp

from ..exceptions import NotFoundError, BadRequestError, NotModifiedError, UnauthorizedError, ForbiddenError, MethodNotAllowedError, RateLimitError, ServerError


class HTTPClient:
    def __init__(self, token: str, version: Union[int, str] = 9, max_retries: int = 4) -> None:
        """
        Instantiate a new HttpApi object.

        :param token: Discord API token

        Keyword Arguments:
        :param version: The discord API version.
                        See https://discord.com/developers/docs/reference#api-versioning.
        :param max_retries: Max amount of attemps after
                            error codes 5xx & 429
        """

        self.header: Dict[str, str] = {"Authorization": f"Bot {token}"}
        self.endpoint: str = f"https://discord.com/api/v{version}"
        self.max_retries: int = max_retries

    # TODO: Retry after rate limit time is up
    async def get(self, route: str) -> Dict:
        """
        :return: JSON response from the discord API.
        """

        async with aiohttp.ClientSession() as session:
            for tries in range(self.max_retries):
                async with session.get(f"{self.endpoint}/{route}", headers=self.header) as resp:

                    if resp.status in [200, 201, 204]:
                        return await resp.json()

                    elif resp.status == 304:
                        raise NotModifiedError

                    elif resp.status == 400:
                        raise BadRequestError

                    elif resp.status == 401:
                        raise UnauthorizedError

                    elif resp.status == 403:
                        raise ForbiddenError

                    elif resp.status == 404:
                        raise NotFoundError

                    elif resp.status == 405:
                        raise MethodNotAllowedError

                    elif resp.status == 429:
                        raise RateLimitError

                    elif resp.status == 502:
                        asyncio.sleep(1 + tries * 2)
                        continue

            raise ServerError("Max retries exceeded")
