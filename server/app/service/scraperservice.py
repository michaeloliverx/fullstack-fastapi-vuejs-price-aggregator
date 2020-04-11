import asyncio
import logging
from typing import Set

import httpx
import selectorlib
from sqlalchemy import orm

from app.models import shopmodels, scrapermodels
from app.service import shopservice
from app.settings import settings

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self, shop: shopmodels.ShopRead) -> None:
        self.protocol = "https"
        self._shop = shop
        self.base_url = f"{self.protocol}://{self._shop.url}"
        self.name = self._shop.name

        # Create Extractor for listing page
        self._listing_page_extractor = selectorlib.Extractor(
            self._shop.listing_page_selector
        )

    def __repr__(self) -> str:
        return f"Scraper(name={self.name}, base_url={self.base_url})"

    def _build_query_url(self, q: str) -> str:
        return self.base_url + self._shop.query_url.format(query=q)

    async def query_listings(
        self, client: httpx.AsyncClient, query: str, limit: int = 10
    ) -> scrapermodels.ShopListings:

        url = self._build_query_url(query)
        html = await fetch_page(url=url, client=client)

        results = self._listing_page_extractor.extract(
            html, base_url=self.base_url
        ).get("items")
        if results:
            results = results[:limit]
        response_object = {
            "id": self._shop.id,
            "name": self._shop.name,
            "listings": results,
        }
        return scrapermodels.ShopListings(id=self._shop.id, name=self._shop.name, listings=results)


async def fetch_page(url: str, client: httpx.AsyncClient):
    """Perform a HTTP GET request on given URL."""
    response = await client.get(url)
    html = response.text
    return html


async def query_scrapers(query: str, limit: int, include: Set[int]):
    """Query scrapers entry point."""

    # Only use one client for all requests
    async with httpx.AsyncClient(verify=False,) as client:
        tasks = [
            scrapers[i].query_listings(client=client, query=query, limit=limit)
            for i in include
        ]
        results = await asyncio.gather(*tasks)
    return results


scrapers = {}


def populate_scrapers(db_session: orm.Session):
    """
    Populate scraper configuration into memory for fast lookup.
    """
    global scrapers
    scrapers = {}
    shops = shopservice.get_multiple(db_session=db_session)
    for shop in shops:
        shop_model = shopmodels.ShopRead.from_orm(shop)
        scrapers[shop.id] = Scraper(shop_model)
