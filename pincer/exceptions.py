# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.
from typing import Optional


class PincerError(Exception):
    """Base exception class for all Pincer errors"""


class InvalidPayload(PincerError):
    """Exception which gets thrown if an invalid payload has been received.
    This means that the data of the payload did not match the expected
    format and/or didn't contain the expected values.
    """


class UnhandledException(PincerError):
    """Exception which gets thrown if an exception wasn't handled.

    Please create an issue on our GitHub
    if this exception gets thrown.
    """

    def __init__(self, specific: str):
        super(UnhandledException, self).__init__(
            specific + " Please report this to the library devs."
        )


class NoExportMethod(PincerError):
    """Exception which gets raised when an `export` method is expected but
    not found in a module.
    """


class CogError(PincerError):
    """Exception base class for errors related to Cogs."""


class CogNotFound(CogError):
    """Exception which gets raised when a cog is trying to be
    loaded/unloaded but is nonexistent.
    """


class CogAlreadyExists(CogError):
    """Exception which gets raised when a cog is already loaded, but is
    trying to be reloaded!
    """


class NoValidSetupMethod(CogError):
    """Exception which gets raised when an `setup` function is expected but
    none was found!
    """


class TooManySetupArguments(CogError):
    """Exception which gets raised when too many arguments were requested
    in a cog its setup function.
    """


class NoCogManagerReturnFound(CogError):
    """Exception which gets raised when no cog return was found from the
    setup function. (are you missing a return statement?)
    """


class CommandError(PincerError):
    """Base class for exceptions which are related to command."""


class CommandCooldownError(CommandError):
    """Exception which gets raised when a command cooldown has not been
    breached.

    Attributes
    ----------
    ctx: :class:`~objects.message.context.MessageContext`
        The context of the error
    """

    def __init__(self, message: str, context):
        self.ctx = context
        super(CommandCooldownError, self).__init__(message)


class CommandIsNotCoroutine(CommandError):
    """Exception raised when the provided command call is not a coroutine."""


class CommandAlreadyRegistered(CommandError):
    """The command which you are trying to register is already registered."""


class CommandDescriptionTooLong(CommandError):
    """The provided command description is too long,
    as it exceeds 100 characters.
    """


class TooManyArguments(CommandError):
    """A command can have a maximum of 25 arguments.
    If this number of arguments gets exceeded, this exception will be raised.
    """


class InvalidArgumentAnnotation(CommandError):
    """The provided argument annotation is not known, so it cannot be used."""


class CommandReturnIsEmpty(CommandError):
    """Cannot return an empty string to an interaction."""


class InvalidCommandGuild(CommandError):
    """The provided guild id not not valid."""


class InteractionDoesNotExist(CommandError):
    """The action which you are trying to perform requires an
    interaction to be created/sent to discord. But this has not been
    done yet!
    """


class UseFollowup(CommandError):
    """A reply has already been sent, please use a followup to
    continue replying.
    """


class InteractionAlreadyAcknowledged(CommandError):
    """The command has already been acknowledged by discord.
    This can be because a reply or ack has already been sent!
    """


class InteractionTimedOut(CommandError):
    """Discord had to wait too long for a response from your command!
    The discord wait time can be extended by using the
    :func:`~pincer.objects.app.interaction.Interaction.ack` function in
    the :attr:`~pincer.objects.message.context.MessageContext.interaction`
    property.
    """


class InvalidCommandName(CommandError):
    """Exception raised when the command is considered invalid.
    This is caused by a name that doesn't match the command name regex.
    """


class InvalidEventName(PincerError):
    """Exception raised when the event name is not a valid event.
    This can be because the event name did not begin with an ``on_`` or
    because it's not a valid event in the library.
    """


class InvalidUrlError(PincerError, ValueError):
    """Exception raised when an invalid url has been provided."""


class ImageEncodingError(PincerError):
    """Exception raised when an image cannot be encoded for Discord"""


class EmbedFieldError(PincerError, ValueError):
    """Exception that is raised when an embed field is too large."""

    @classmethod
    def from_desc(cls, _type: str, max_size: int, cur_size: int):
        """Create an instance by description.

        Parameters
        ----------
        _type :class:`str`
            The type/name of the field.
        max_si :class:`int`
            The maximum size of the field.
        cur_size :class:`int`
            The current size of the field.
        """
        return cls(
            f"{_type} can have a maximum length of {max_size}."
            f" (Current size: {cur_size})"
        )


class EmbedOverflow(PincerError):
    """Exception that is raised when too many embeds are passed in."""


class TaskError(PincerError):
    """Base class for exceptions that are related to task.

    Attributes
    ----------
    task: :class:`~utils.tasks.Task`
        The task that raised the exception.
    """

    def __init__(self, message: str, task=None):
        self.task = task
        super().__init__(message)


class TaskAlreadyRunning(TaskError):
    """Exception that is raised when the user tries to start a running task."""


class TaskCancelError(TaskError):
    """Exception that is raised when a task cannot be cancelled."""


class TaskIsNotCoroutine(TaskError):
    """Exception that is raised when the provided function for a task is not
    a coroutine.
    """


class TaskInvalidDelay(TaskError):
    """Exception that is raised when the provided delay is invalid."""


class DispatchError(PincerError):
    """Base exception class for all errors which are specifically related
    to the dispatcher.
    """


class _InternalPerformReconnectError(DispatchError):
    """Internal helper exception which on raise lets the client reconnect."""


class DisallowedIntentsError(DispatchError):
    """Invalid gateway intent got provided.
    Make sure your client has the enabled intent.
    """


class InvalidTokenError(DispatchError, ValueError):
    """Exception raised when the authorization token is invalid."""

    def __init__(self, hint: Optional[str] = None):
        hint = hint or ''

        super(InvalidTokenError, self).__init__(
            "The given token is not a valid token.\n" + hint
        )


class HeartbeatError(DispatchError):
    """Exception raised due to a problem with websocket heartbeat."""


class UnavailableGuildError(PincerError):
    """Exception raised due to a guild being unavailable.
    This is caused by a discord outage.
    """


class TimeoutError(PincerError):
    """Exception raised when :class:`~pincer.utils.event_mgr.EventMgr`
    `wait_for` and `loop_for` methods time out
    """


class GatewayConnectionError(PincerError):
    """Could not connect to Discord gateway"""


# Discord HTTP Errors
# `developers/docs/topics/opcodes-and-status-codes#http`


class HTTPError(PincerError):
    """HTTP Exception base class."""


class NotModifiedError(HTTPError):
    """Error code 304."""


class BadRequestError(HTTPError):
    """Error code 400."""


class UnauthorizedError(HTTPError):
    """Error code 401."""


class ForbiddenError(HTTPError):
    """Error code 403."""


class NotFoundError(HTTPError):
    """Error code 404."""


class MethodNotAllowedError(HTTPError):
    """Error code 405."""


class RateLimitError(HTTPError):
    """Error code 429."""


class GatewayError(HTTPError):
    """Error code 502."""


class ServerError(HTTPError):
    """Error code 5xx."""
