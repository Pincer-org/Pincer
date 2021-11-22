
.. currentmodule:: pincer.commands

Pincer Commands Module
==================

Commands
--------

command
~~~~~~~

.. autofunction:: command
    :decorator:

Command Types
-------------

.. autoclass:: CommandArg()
    :exclude-members: get_payload
.. autoclass:: Description()
    :exclude-members: get_payload
.. autoclass:: Choice()
    :exclude-members: get_payload
.. autoclass:: Choices()
    :exclude-members: get_payload
.. autoclass:: ChannelTypes()
    :exclude-members: get_payload
.. autoclass:: MaxValue()
    :exclude-members: get_payload
.. autoclass:: MinValue()
    :exclude-members: get_payload

ChatCommandHandler
~~~~~~~~~~~~~~~~~~

.. attributetable:: ChatCommandHandler

.. autoclass:: ChatCommandHandler()