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

import requests
from requests.models import Response

from ..exceptions import NotFoundError, BadRequestError, NotModifiedError, UnauthorizedError, ForbiddenError, MethodNotAllowedError, RateLimitError, GatewayError, ServerError


class HTTPClient:
    def __init__(self, token: str, version: Union[int, str] = 9) -> None:
        """
        Instantiate a new HttpApi object.

        :param version: The discord API version.
                        See https://discord.com/developers/docs/reference#api-versioning.
        :param token: Discord API token
        """

        self.header: Dict[str, str] = {"Authorization": f"Bot {token}"}
        self.endpoint: str = f"https://discord.com/api/v{version}"

    # TODO: Retry on error code 5xx
    # TODO: Retry after rate limit time is up
    def get(self, route: str) -> Dict:
        """
        :return: JSON response from the discord API.
        """

        res: Response = requests.get(
            f"{self.endpoint}/{route}", headers=self.header)

        if res.status_code in [200, 201, 204]:
            return res.json()
        elif res.status_code == 304:
            raise NotModifiedError
        elif res.status_code == 400:
            raise BadRequestError
        elif res.status_code == 401:
            raise UnauthorizedError
        elif res.status_code == 403:
            raise ForbiddenError
        elif res.status_code == 404:
            raise NotFoundError
        elif res.status_code == 405:
            raise MethodNotAllowedError
        elif res.status_code == 429:
            raise RateLimitError
        elif res.status_code == 502:
            raise GatewayError
        else:
            raise ServerError
