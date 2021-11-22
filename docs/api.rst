.. currentmodule:: pincer

API Reference
==============

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

pincer.core
------------

Dispatching
-----------

GatewayDispatch
~~~~~~~~~~~~~~~

.. attributetable:: GatewayDispatch

.. autoclass:: GatewayDispatch()

Gateway
-------

Dispatcher
~~~~~~~~~~

.. attributetable:: Dispatcher

.. autoclass:: Dispatcher()
    :exclude-members: __handler_manager, __dispatcher

Heartbeat
---------

Heartbeat
~~~~~~~~~

.. attributetable:: Heartbeat

.. autoclass:: Heartbeat()
    :exclude-members: __send

Http
----

HTTPClient
~~~~~~~~~~

.. attributetable:: HTTPClient

.. autoclass:: HTTPClient()
    :exclude-members: __send, __handle_response


pincer.middleware
------------------

Activity Join Request
---------------------

.. note::
   Not implemented yet.

Activity Join
-------------

.. note::
   Not implemented yet.

Activity Spectate
-----------------

.. note::
   Not implemented yet.

Channel Create
--------------

channel_create_middleware
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.channel_create.channel_create_middleware

Error
-----

error_middleware
~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.error.error_middleware

Guild Create
------------

guild_create_middleware
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.guild_create.guild_create_middleware

Guild Status
------------

.. note::
   Not implemented yet.

Interaction Create
------------------

convert_message
~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.interaction_create.convert_message

interaction_response_handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.interaction_create.interaction_response_handler

interaction_handler
~~~~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.interaction_create.interaction_handler

interaction_create_middleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.interaction_create.interaction_create_middleware

Message Create
--------------

message_create_middleware
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.message_create.message_create_middleware

Message Delete
--------------

on_message_delete_middleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.message_delete.on_message_delete_middleware

Message Update
--------------

message_update_middleware
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.message_update.message_update_middleware

Notification Create
-------------------

.. note::
   Not implemented yet.

Payload
-------

payload_middleware
~~~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.payload.payload_middleware

Ready
-----

on_ready_middleware
~~~~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.ready.on_ready_middleware

Speaking Start
--------------

.. note::
   Not implemented yet.

Speaking Stop
-------------

.. note::
   Not implemented yet.

Voice Channel Select
--------------------

.. note::
   Not implemented yet.

Voice Connection Status
-----------------------

.. note::
   Not implemented yet.

Voice Settings Update
---------------------

.. note::
   Not implemented yet.

Voice State Create
------------------

.. note::
   Not implemented yet.

Voice State Delete
------------------

.. note::
   Not implemented yet.

Voice State Update
------------------

voice_state_update_middleware
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pincer.middleware.voice_state_update.voice_state_update_middleware

pincer.utils
===============

Api Object
----------

APIObject
~~~~~~~~~

.. attributetable:: APIObject

.. autoclass:: APIObject()

Directory
---------

chdir
~~~~~

.. autofunction:: chdir

Signature
---------

get_signature_and_params
~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: get_signature_and_params

get_params
~~~~~~~~~~

.. autofunction:: get_params

Snowflake
---------

Snowflake
~~~~~~~~~

.. attributetable:: Snowflake

.. autoclass:: Snowflake()

Tasks
-----

Task
~~~~

.. attributetable:: Task

.. autoclass:: Task()

TaskScheduler
~~~~~~~~~~~~~

.. attributetable:: TaskScheduler

.. autoclass:: TaskScheduler()
   :exclude-members: loop

   .. automethod:: TaskScheduler.loop
      :decorator:

Timestamp
---------

Timestamp
~~~~~~~~~

.. attributetable:: Timestamp

.. autoclass:: Timestamp()

Types
-----

MissingType
~~~~~~~~~~~

.. autoclass:: MissingType()

MISSING
~~~~~~~

.. data:: MISSING
   :type: MissingType

APINullable
~~~~~~~~~~~

.. data:: APINullable
   :type: Union[T, MissingType]

   Represents a value which is optionally returned from the API

Coro
~~~~

.. data:: Coro
   :type: TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])

   Represents a coroutine.

choice_value_types
~~~~~~~~~~~~~~~~~~

.. data:: choice_value_types
   :type: Tuple[str, int, float]
