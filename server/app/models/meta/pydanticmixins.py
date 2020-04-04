from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PydanticTS(BaseModel):
    created_at: datetime
    updated_at: Optional[datetime]
