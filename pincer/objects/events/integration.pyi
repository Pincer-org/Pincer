from ...utils.api_object import APIObject as APIObject, GuildProperty as GuildProperty
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING

class IntegrationDeleteEvent(APIObject, GuildProperty):
    id: Snowflake
    guild_id: Snowflake
    application_id: APINullable[Snowflake]

class IntegrationCreateEvent(APIObject, GuildProperty):
    id: Snowflake
    guild_id: Snowflake
    application_id: APINullable[Snowflake]

class IntegrationUpdateEvent(APIObject, GuildProperty):
    id: Snowflake
    guild_id: Snowflake
    application_id: APINullable[Snowflake]
