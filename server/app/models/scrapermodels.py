import logging
import re
from typing import List, Optional

from pydantic import BaseModel, validator

from .meta.pydanticbase import PydanticBase

logger = logging.getLogger(__name__)

# Matching 00p in currency
CURRENCY_PENCE_REGEX = re.compile(r"(\d{2})[p]")

# Matches any whitespace characters and £ symbol
CURRENCY_WHITESPACE_REGEX = re.compile(r"[£()\s+]")


class ScrapedItem(PydanticBase):
    name: Optional[str] = None
    url: Optional[str] = None
    price: Optional[str] = None
    price_per_unit: Optional[str] = None
    image_url: Optional[str] = None

    @validator("price")
    def format_p(cls, v):
        """Transforms varying pricing formats to #.##"""
        if v:
            v = re.sub(CURRENCY_WHITESPACE_REGEX, "", v)
            match = re.match(CURRENCY_PENCE_REGEX, v)
            if match:
                v = f"0.{match.group(1)}"
            return v

    @validator("price_per_unit")
    def format_ppu(cls, v):
        if v:
            v = re.sub(CURRENCY_WHITESPACE_REGEX, "", v)
            v = v.replace("per", "/")
            return v

    @validator("*", pre=True)
    def filter_invalid_values(cls, v):
        if isinstance(v, list):
            return None
        return v


class ShopListings(BaseModel):
    id: int
    name: str
    listings: Optional[List[ScrapedItem]] = None
