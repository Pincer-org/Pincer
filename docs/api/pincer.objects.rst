.. currentmodule:: pincer

Pincer Objects Module
----------------------

Pincer Objects App Section
----------------------------

Applications
------------

Application
~~~~~~~~~~~

.. attributetable:: pincer.objects.app.Application

.. autoclass:: pincer.objects.app.Application()

Commands
--------

AppCommandType
~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.AppCommandType

.. autoclass:: pincer.objects.app.AppCommandType()

AppCommandOptionType
~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.AppCommandOptionType

.. autoclass:: pincer.objects.app.AppCommandOptionType()

AppCommandInteractionDataOption
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.AppCommandInteractionDataOption

.. autoclass:: pincer.objects.app.AppCommandInteractionDataOption()

AppCommandOption
~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.AppCommandOption

.. autoclass:: pincer.objects.app.AppCommandOption()

AppCommand
~~~~~~~~~~

.. attributetable:: pincer.objects.app.AppCommand

.. autoclass:: pincer.objects.app.AppCommand()

ClientCommandStructure
~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.ClientCommandStructure

.. autoclass:: pincer.objects.app.ClientCommandStructure()

Intents
-------

Intents
~~~~~~~

.. attributetable:: pincer.objects.app.Intents

.. autoclass:: pincer.objects.app.Intents()

Interaction Base
----------------

CallbackType
~~~~~~~~~~~~

.. attributetable:: CallbackType

.. autoclass:: pincer.objects.app.CallbackType()

InteractionType
~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.InteractionType

.. autoclass:: pincer.objects.app.InteractionType()

MessageInteraction
~~~~~~~~~~~~~~~~~~

.. autoclass:: pincer.objects.app.InteractionFlags()

ResolvedData
~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.ResolvedData

.. autoclass:: pincer.objects.app.ResolvedData()

InteractionData
~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.InteractionData

.. autoclass:: pincer.objects.app.InteractionData()

Interaction
~~~~~~~~~~~

.. attributetable:: pincer.objects.app.Interaction

.. autoclass:: pincer.objects.app.Interaction()

Select Menu
-----------

SelectOption
~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.SelectOption

.. autoclass:: pincer.objects.app.SelectOption()

SelectMenu
~~~~~~~~~~

.. attributetable:: pincer.objects.app.SelectMenu

.. autoclass:: pincer.objects.app.SelectMenu()

Session Start Limit
-------------------

SessionStartLimit
~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.SessionStartLimit

.. autoclass:: pincer.objects.app.SessionStartLimit()

Throttle Scope
--------------

ThrottleScope
~~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.ThrottleScope

.. autoclass:: pincer.objects.app.throttleScope()

Throttling
----------

ThrottleInterface
~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.ThrottleInterface

.. autoclass:: pincer.objects.app.ThrottleInterface()

DefaultThrottleHandler
~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.app.DefaultThrottleHandler

.. autoclass:: pincer.objects.app.DefaultThrottleHandler()


Pincer Objects Events Section
-------------------------------

Channel
-------

ChannelPinsUpdateEvent
~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ChannelPinsUpdateEvent

.. autoclass:: pincer.objects.events.ChannelPinsUpdateEvent()

Error
-----

DiscordError
~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.DiscordError

.. autoclass:: pincer.objects.events.DiscordError()

Gateway Commands
----------------

Identify
~~~~~~~~

.. attributetable:: pincer.objects.events.Identify

.. autoclass:: pincer.objects.events.Identify()

Resume
~~~~~~

.. attributetable:: pincer.objects.events.Resume

.. autoclass:: pincer.objects.events.Resume()

Guild
-----

GuildBanAddEvent
~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.GuildBanAddEvent

.. autoclass:: pincer.objects.events.GuildBanAddEvent()

GuildBanRemoveEvent
~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.GuildBanRemoveEvent

.. autoclass:: pincer.objects.events.GuildBanRemoveEvent()

GuildEmojisUpdateEvent
~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.GuildEmojisUpdateEvent

.. autoclass:: pincer.objects.events.GuildEmojisUpdateEvent()

GuildStickersUpdateEvent
~~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.GuildStickersUpdateEvent

.. autoclass:: pincer.objects.events.GuildStickersUpdateEvent()

GuildIntegrationsUpdateEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.GuildIntegrationsUpdateEvent

.. autoclass:: pincer.objects.events.GuildIntegrationsUpdateEvent()

GuildMemberRemoveEvent
~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.GuildMemberRemoveEvent

.. autoclass:: pincer.objects.events.GuildMemberRemoveEvent()

GuildMemberUpdateEvent
~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.GuildMemberUpdateEvent

.. autoclass:: pincer.objects.events.GuildMemberUpdateEvent()

GuildMembersChunkEvent
~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.GuildMembersChunkEvent

.. autoclass:: pincer.objects.events.GuildMembersChunkEvent()

GuildRoleCreateEvent
~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.GuildRoleCreateEvent

.. autoclass:: pincer.objects.events.GuildRoleCreateEvent()

GuildRoleUpdateEvent
~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.GuildRoleUpdateEvent

.. autoclass:: pincer.objects.events.GuildRoleUpdateEvent()

GuildRoleDeleteEvent
~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.GuildRoleDeleteEvent

.. autoclass:: pincer.objects.events.GuildRoleDeleteEvent()

Hello Ready
-----------

HelloEvent
~~~~~~~~~~

.. attributetable:: pincer.objects.events.HelloEvent

.. autoclass:: pincer.objects.events.HelloEvent()

ReadyEvent
~~~~~~~~~~

.. attributetable:: pincer.objects.events.ReadyEvent

.. autoclass:: pincer.objects.events.ReadyEvent()

integration
-----------

IntegrationDeleteEvent
~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.IntegrationDeleteEvent

.. autoclass:: pincer.objects.events.IntegrationDeleteEvent()

Invite
------

InviteCreateEvent
~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.InviteCreateEvent

.. autoclass:: pincer.objects.events.InviteCreateEvent()

InviteDeleteEvent
~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.InviteDeleteEvent

.. autoclass:: pincer.objects.events.InviteDeleteEvent()

Message
-------

MessageDeleteEvent
~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.MessageDeleteEvent

.. autoclass:: pincer.objects.events.MessageDeleteEvent()

MessageDeleteBulkEvent
~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.MessageDeleteBulkEvent

.. autoclass:: pincer.objects.events.MessageDeleteBulkEvent()

MessageReactionAddEvent
~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.MessageReactionAddEvent

.. autoclass:: pincer.objects.events.MessageReactionAddEvent()

MessageReactionRemoveEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.MessageReactionRemoveEvent

.. autoclass:: pincer.objects.events.MessageReactionRemoveEvent()

MessageReactionRemoveAllEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.MessageReactionRemoveAllEvent

.. autoclass:: pincer.objects.events.MessageReactionRemoveAllEvent()

MessageReactionRemoveEmojiEvent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.MessageReactionRemoveEmojiEvent

.. autoclass:: pincer.objects.events.MessageReactionRemoveEmojiEvent()

Presence
--------

ActivityType
~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ActivityType

.. autoclass:: pincer.objects.events.ActivityType()

ActivityTimestamp
~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ActivityTimestamp

.. autoclass:: pincer.objects.events.ActivityTimestamp()

ActivityEmoji
~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ActivityEmoji

.. autoclass:: pincer.objects.events.ActivityEmoji()

ActivityParty
~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ActivityParty

.. autoclass:: pincer.objects.events.ActivityParty()

ActivityAssets
~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ActivityAssets

.. autoclass:: pincer.objects.events.ActivityAssets()

ActivitySecrets
~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ActivitySecrets

.. autoclass:: pincer.objects.events.ActivitySecrets()

ActivityFlags
~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ActivityFlags

.. autoclass:: pincer.objects.events.ActivityFlags()

ActivityButton
~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ActivityButton

.. autoclass:: pincer.objects.events.ActivityButton()

Activity
~~~~~~~~

.. attributetable:: pincer.objects.events.Activity

.. autoclass:: pincer.objects.events.Activity()

ClientStatus
~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ClientStatus

.. autoclass:: pincer.objects.events.ClientStatus()

PresenceUpdateEvent
~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.PresenceUpdateEvent

.. autoclass:: pincer.objects.events.PresenceUpdateEvent()

Thread
------

ThreadListSyncEvent
~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ThreadListSyncEvent

.. autoclass:: pincer.objects.events.ThreadListSyncEvent()

ThreadMembersUpdateEvent
~~~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.ThreadMembersUpdateEvent

.. autoclass:: pincer.objects.events.ThreadMembersUpdateEvent()

Typing Start
------------

TypingStartEvent
~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.TypingStartEvent

.. autoclass:: pincer.objects.events.TypingStartEvent()

Voice
-----

VoiceServerUpdateEvent
~~~~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.VoiceServerUpdateEvent

.. autoclass:: pincer.objects.events.VoiceServerUpdateEvent()

Webhook
-------

WebhooksUpdateEvent
~~~~~~~~~~~~~~~~~~~

.. attributetable:: pincer.objects.events.WebhooksUpdateEvent

.. autoclass:: pincer.objects.events.WebhooksUpdateEvent()

