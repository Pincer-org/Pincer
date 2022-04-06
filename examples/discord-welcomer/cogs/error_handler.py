"""
Processes all exceptions that occur in runtime.
"""
import logging

from pincer import Cog, Client


class ErrorHandler(Cog):
    @Client.event
    async def on_error(self, error: Exception, *args, **kwargs):
        # You should probably handle this more specific
        logging.error(error)
