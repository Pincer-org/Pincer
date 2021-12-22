from ...utils.api_object import APIObject as APIObject
from ...utils.snowflake import Snowflake as Snowflake
from ...utils.types import APINullable as APINullable, MISSING as MISSING
from typing import Optional

class Attachment(APIObject):
    id: Snowflake
    filename: str
    size: int
    url: str
    proxy_url: str
    content_type: APINullable[str]
    height: APINullable[Optional[int]]
    width: APINullable[Optional[int]]
