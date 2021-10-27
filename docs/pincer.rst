.. currentmodule:: pincer

Pincer Module
=============

Clients
-------

Client
~~~~~~

.. attributetable:: Client

.. autoclass:: Client
    :exclude-members: event

    .. automethod:: Client.event()
        :decorator:

Commands
--------

command
~~~~~~~

.. autofunction:: command
    :decorator:

ChatCommandHandler
~~~~~~~~~~~~~~~~~~

.. attributetable:: ChatCommandHandler

.. autoclass:: ChatCommandHandler()

Exceptions
----------

.. autoexception:: PincerError()

.. autoexception:: UnhandledException()

.. autoexception:: NoExportMethod()

.. autoexception:: CogError()

.. autoexception:: CogNotFound()

.. autoexception:: CogAlreadyExists()

.. autoexception:: NoValidSetupMethod()

.. autoexception:: TooManySetupArguments()

.. autoexception:: NoCogManagerReturnFound()

.. autoexception:: CommandError()

.. autoexception:: CommandCooldownError()

.. autoexception:: CommandIsNotCoroutine()

.. autoexception:: CommandAlreadyRegistered()

.. autoexception:: CommandDescriptionTooLong()

.. autoexception:: TooManyArguments()

.. autoexception:: InvalidArgumentAnnotation()

.. autoexception:: CommandReturnIsEmpty()

.. autoexception:: InvalidCommandGuild()

.. autoexception:: InvalidCommandName()

.. autoexception:: InvalidEventName()

.. autoexception:: InvalidUrlError()

.. autoexception:: EmbedFieldError()
    :exclude-members: from_desc

.. autoexception:: TaskError()

.. autoexception:: TaskAlreadyRunning()

.. autoexception:: TaskCancelError()

.. autoexception:: TaskIsNotCoroutine()

.. autoexception:: TaskInvalidDelay()

.. autoexception:: DispatchError()

.. autoexception:: DisallowedIntentsError()

.. autoexception:: InvalidTokenError()

.. autoexception:: HeartbeatError()

.. autoexception:: UnavailableGuildError()

.. autoexception:: HTTPError()

.. autoexception:: NotModifiedError()

.. autoexception:: BadRequestError()

.. autoexception:: UnauthorizedError()

.. autoexception:: ForbiddenError()

.. autoexception:: NotFoundError()

.. autoexception:: MethodNotAllowedError()

.. autoexception:: RateLimitError()

.. autoexception:: GatewayError()

.. autoexception:: ServerError()

Exception Hierarchy
~~~~~~~~~~~~~~~~~~~

.. exception_hierarchy::

    - :exc:`Exception`
        - :exc:`PincerError`
            - :exc: `InvalidPayload`
            - :exc:`UnhandledException`
            - :exc:`NoExportMethod`
            - :exc:`CogError`
                - :exc:`CogNotFound`
                - :exc:`CogAlreadyExists`
                - :exc:`NoValidSetupMethod`
                - :exc:`TooManySetupArguments`
                - :exc:`NoCogManagerReturnFound`
            - :exc:`CommandError`
                - :exc:`CommandCooldownError`
                - :exc:`CommandIsNotCoroutine`
                - :exc:`CommandAlreadyRegistered`
                - :exc:`CommandDescriptionTooLong`
                - :exc:`TooManyArguments`
                - :exc:`InvalidArgumentAnnotation`
                - :exc:`CommandReturnIsEmpty`
                - :exc:`InvalidCommandGuild`
                - :exc:`InvalidCommandName`
            - :exc:`InvalidEventName`
            - :exc:`InvalidUrlError`
            - :exc:`EmbedFieldError`
            - :exc:`TaskError`
                - :exc:`TaskAlreadyRunning`
                - :exc:`TaskCancelError`
                - :exc:`TaskIsNotCoroutine`
                - :exc:`TaskInvalidDelay`
            - :exc:`DispatchError`
                - :exc:`DisallowedIntentsError`
                - :exc:`InvalidTokenError`
                - :exc:`HeartbeatError`
            - :exc:`UnavailableGuildError`
            - :exc:`HTTPError`
                - :exc:`NotModifiedError`
                - :exc:`BadRequestError`
                - :exc:`UnauthorizedError`
                - :exc:`ForbiddenError`
                - :exc:`NotFoundError`
                - :exc:`MethodNotAllowedError`
                - :exc:`RateLimitError`
                - :exc:`GatewayError`
                - :exc:`ServerError`