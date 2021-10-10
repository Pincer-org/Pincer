# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

import asyncio
import logging
from asyncio import sleep
from json import dumps
from typing import Dict, Any, Optional, Protocol, Union

from aiohttp import ClientSession, ClientResponse
from aiohttp.client import _RequestContextManager
from aiohttp.payload import Payload
from aiohttp.typedefs import StrOrURL

from . import __package__
from .._config import GatewayConfig
from ..exceptions import (
    NotFoundError, BadRequestError, NotModifiedError, UnauthorizedError,
    ForbiddenError, MethodNotAllowedError, RateLimitError, ServerError,
    HTTPError
)

_log = logging.getLogger(__package__)


class HttpCallable(Protocol):
    """aiohttp HTTP method"""
    __name__: str

    def __call__(
            self, url: StrOrURL, *,
            allow_redirects: bool = True,
            method: Optional[Union[Dict, str, Payload]] = None,
            **kwargs: Any
    ) -> _RequestContextManager:
        ...


class HTTPClient:
    """Interacts with Discord API through HTTP protocol"""

    def __init__(self, token: str, *, version: int = None, ttl: int = 5):
        """
        Instantiate a new HttpApi object.

        :param token:
            Discord API token

        Keyword Arguments:

        :param version:
            The discord API version.
            See `<https://discord.com/developers/docs/reference#api-versioning>`_.

        :param ttl:
            Max amount of attempts after error code 5xx
        """
        version = version or GatewayConfig.version
        self.url: str = f"https://discord.com/api/v{version}"
        self.max_ttl: int = ttl

        headers: Dict[str, str] = {
            "Authorization": f"Bot {token}",
        }
        self.__session: ClientSession = ClientSession(headers=headers)

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
        """Closes :attr:`~.HTTPClient.__session`"""
        await self.__session.close()

    async def __send(
            self,
            method: HttpCallable,
            endpoint: str, *,
            content_type: str = "application/json",
            data: Optional[Union[Dict, str, Payload]] = None,
            __ttl: int = None
    ) -> Optional[Dict]:
        """
        Send an api request to the Discord REST API.

        :meta public:

        :param method:
            The method for the request. (eg GET or POST)

        :param endpoint:
            The endpoint to which the request will be sent.

        Keyword Arguments:

        :param content_type:
            The request's content type.

        :param data:
            The data which will be added to the request.

        :param __ttl:
            Private param used for recursively setting the retry amount.
            (Eg set to 1 for 1 max retry)
        """
        ttl = __ttl or self.max_ttl

        if ttl == 0:
            logging.error(
                # TODO: print better method name
                f"{method.__name__.upper()} {endpoint} has reached the "
                f"maximum retry count of {self.max_ttl}."
            )

            raise ServerError(f"Maximum amount of retries for `{endpoint}`.")

        if isinstance(data, dict):
            data = dumps(data)

        # TODO: print better method name
        # TODO: Adjust to work non-json types
        _log.debug(f"{method.__name__.upper()} {endpoint} | {data}")

        url = f"{self.url}/{endpoint}"
        async with method(
                url,
                data=data,
                headers={"Content-Type": content_type}
        ) as res:
            return await self.__handle_response(
                res, method, endpoint, content_type, data, ttl
            )

    async def __handle_response(
            self,
            res: ClientResponse,
            method: HttpCallable,
            endpoint: str,
            content_type: str,
            data: Optional[str],
            __ttl: int,
    ) -> Optional[Dict]:
        """
        Handle responses from the discord API.

        :meta public:

        Side effects:
            If a 5xx error code is returned it will retry the request.

        :param res:
            The response from the discord API.

        :param method:
            The method which was used to call the endpoint.

        :param endpoint:
            The endpoint to which the request was sent.

        :param content_type:
            The request's content type.

        :param data:
            The data which was added to the request.

        :param __ttl:
            Private param used for recursively setting the retry amount.
            (Eg set to 1 for 1 max retry)
        """
        _log.debug(f"Received response for {endpoint} | {await res.text()}")
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
            if isinstance(exception, RateLimitError):
                timeout = (await res.json()).get("retry_after", 40)

                _log.exception(
                    f"RateLimitError: {res.reason}."
                    f" Retrying in {timeout} seconds"
                )
                await sleep(timeout)
                return await self.__send(
                    method,
                    endpoint,
                    content_type=content_type,
                    data=data
                )

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
        return await self.__send(
            method,
            endpoint,
            content_type=content_type,
            __ttl=__ttl - 1,
            data=data
        )

    async def delete(self, route: str) -> Optional[Dict]:
        """
        Sends a delete request to a Discord REST endpoint.

        :param route:
            The Discord REST endpoint to send a delete request to.

        :return:
            JSON response from the discord API.
        """
        return await self.__send(self.__session.delete, route)

    async def get(self, route: str) -> Optional[Dict]:
        """
        Sends a get request to a Discord REST endpoint.

        :param route:
            The Discord REST endpoint to send a get request to.

        :return:
            JSON response from the discord API.
        """
        return await self.__send(self.__session.get, route)

    async def head(self, route: str) -> Optional[Dict]:
        """
        Sends a head request to a Discord REST endpoint.

        :param route:
            The Discord REST endpoint to send a head request to.

        :return:
            JSON response from the discord API.
        """
        return await self.__send(self.__session.head, route)

    async def options(self, route: str) -> Optional[Dict]:
        """
        Sends a options request to a Discord REST endpoint.

        :param route:
            The Discord REST endpoint to send a options request to.

        :return:
            JSON response from the discord API.
        """
        return await self.__send(self.__session.options, route)

    async def patch(
            self,
            route: str,
            data: Dict,
            content_type: str = "application/json"
    ) -> Optional[Dict]:
        """
        Sends a patch request to a Discord REST endpoint.

        :param route:
            The Discord REST endpoint to send a patch request to.

        :param data:
            The update data for the patch request.

        :param content_type:
            Body content type.

        :return:
            JSON response from the discord API.
        """
        return await self.__send(
            self.__session.patch,
            route,
            content_type=content_type,
            data=data
        )

    async def post(
            self,
            route: str,
            data: Dict,
            content_type: str = "application/json"
    ) -> Optional[Dict]:
        """
        Sends a post request to a Discord REST endpoint.

        :param route:
            The Discord REST endpoint to send a post request to.

        :param data:
            The data for the post request.

        :param content_type:
            Body content type.

        :return:
            JSON response from the discord API.
        """
        return await self.__send(
            self.__session.post,
            route,
            content_type=content_type,
            data=data
        )

    async def put(
            self,
            route: str,
            data: Dict,
            content_type: str = "application/json"
    ) -> Optional[Dict]:
        """
        Sends a put request to a Discord REST endpoint.

        :param route:
            The Discord REST endpoint to send a put request to.

        :param data:
            The data for the put request.

        :param content_type:
            Body content type.

        :return:
            JSON response from the discord API.
        """
        return await self.__send(
            self.__session.put,
            route,
            content_type=content_type,
            data=data
        )
