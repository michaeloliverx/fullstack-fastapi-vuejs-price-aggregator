from datetime import datetime

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    """
    orjson.dumps returns bytes, to match standard json.dumps we need to decode.
    orjson.dumps option arguments provide many options such as `option=orjson.OPT_SERIALIZE_UUID` to natively encode UUID instances.
    """
    return orjson.dumps(v, default=default).decode()


class PydanticBase(BaseModel):
    """PydanticBase with custom JSON implementation.
    'orjson' is used here as it takes care of datetime
    encoding natively and gives better (de)serialisation performance.

    .. seealso::

        https://pydantic-docs.helpmanual.io/usage/exporting_models/#custom-json-deserialisation

    """

    class Config:
        orm_mode = True
        validate_assignment = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
