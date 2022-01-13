
.. currentmodule:: pincer.commands

Pincer Commands Module
======================

Commands
--------

command
~~~~~~~

.. autofunction:: command
    :decorator:
.. autofunction:: message_command
    :decorator:
.. autofunction:: user_command
    :decorator:

Command Types
-------------

.. autoclass:: Modifier()
.. autoclass:: Description()
.. autoclass:: Choices()
.. autoclass:: Choice()
.. autoclass:: MaxValue()
.. autoclass:: MinValue()
.. autoclass:: ChannelTypes()
.. autoclass:: CommandArg()

ChatCommandHandler
------------------

.. attributetable:: ChatCommandHandler

.. autoclass:: ChatCommandHandler()


Message Components
~~~~~~~~~~~~~~~~~~
.. currentmodule:: pincer.commands.components

.. autoclass:: ActionRow()
.. autoclass:: Button()
    :inherited-members:
.. autoclass:: LinkButton()
.. autoclass:: ButtonStyle()
.. autoclass:: SelectMenu()
    :inherited-members:
.. autoclass:: SelectOption()

.. currentmodule:: pincer.commands.components._component
.. autoclass:: _Component()

.. currentmodule:: pincer.commands.components

.. autofunction:: button
    :decorator:
.. autofunction:: select_menu
    :decorator:
.. autofunction:: component
    :decorator:

Command Groups
~~~~~~~~~~~~~~
.. currentmodule:: pincer.commands.groups

.. autoclass:: Group()
.. autoclass:: Subgroup()