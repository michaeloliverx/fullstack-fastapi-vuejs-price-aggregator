from datetime import datetime

from pydantic import BaseModel


class PydanticTS(BaseModel):
    created_at: datetime
    updated_at: datetime
