from ...utils import APIObject as APIObject
from ...utils.snowflake import Snowflake as Snowflake

class Overwrite(APIObject):
    id: Snowflake
    type: int
    allow: str
    deny: str
