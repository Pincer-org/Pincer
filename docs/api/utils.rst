.. currentmodule:: pincer.utils

Pincer Utils Module
===================

Api Object
----------

APIObject
~~~~~~~~~

.. attributetable:: APIObject

.. autoclass:: APIObject()

APIObject Properties
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: ChannelProperty()

.. autoclass:: GuildProperty()



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
