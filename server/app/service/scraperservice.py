import asyncio
import logging
from typing import Set

import httpx
import pyppeteer
import selectorlib
from app.core.settings import settings
from app.crud import shop_crud
from app.schemas.shop import ShopConfigurationDB

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self, config: ShopConfigurationDB) -> None:
        self.protocol = "https"
        self._config = config
        self.base_url = f"{self.protocol}://{self._config.url}"
        self.name = self._config.name

        # Create Extractor for listing page
        self._listing_page_extractor = selectorlib.Extractor(
            self._config.listing_page_selector
        )

    def __repr__(self) -> str:
        return f"Scraper(name={self.name}, base_url={self.base_url})"

    def _build_query_url(self, q: str) -> str:
        return self.base_url + self._config.query_url.format(query=q)

    async def query_listings(
        self, client: httpx.AsyncClient, query: str, limit: int = 10
    ) -> dict:

        url = self._build_query_url(query)

        # Render page with `pyppeteer` if needed
        if self._config.render_javascript:
            html = await render_page(url=url)
        else:
            html = await fetch_page(url=url, client=client)

        results = self._listing_page_extractor.extract(
            html, base_url=self.base_url
        ).get("items")
        if results:
            results = results[:limit]
        response_object = {
            "id": self._config.id,
            "name": self._config.name,
            "listings": results,
        }
        return response_object


async def fetch_page(url: str, client: httpx.AsyncClient):
    """Perform a HTTP GET request on given URL."""
    response = await client.get(url)
    html = response.text
    return html


async def render_page(url: str) -> str:
    """
    Using ``pyppeteer`` load a web page and return HTML content.
    """
    options = {
        "timeout": int(settings.scraper.PYPPETEER_TIMEOUT * 1000),
        "waitUntil": "domcontentloaded",
    }
    browser = await pyppeteer.launch(
        executablePath=settings.CHROME_BIN, ignoreHTTPSErrors=True, headless=True
    )
    page = await browser.newPage()
    await page.goto(url, options=options)
    await asyncio.sleep(settings.scraper.PYPPETEER_SLEEP)
    html = await page.content()
    await browser.close()
    return html


async def query_scrapers(query: str, limit: int, include: Set[int]):
    """Query scrapers entry point."""

    # Only use one client for all requests
    async with httpx.AsyncClient(
        verify=False, timeout=settings.scraper.HTTPCLIENT_TIMEOUT
    ) as client:
        tasks = [
            scrapers[i].query_listings(client=client, query=query, limit=limit)
            for i in include
        ]
        results = await asyncio.gather(*tasks)
    return results


scrapers = {}


async def initialise():
    """
    Reads all shop configurations from database and using each config initialise's a `Scraper` instance.
    Local scraper dict is then used for quick lookup. Key is scraper id and value is `Scraper` instance.
    Should be called every time new configurations are added to db.
    """
    global scrapers
    scrapers = {}
    shops = await shop_crud.read_all()
    for s in shops:
        scrapers[s["id"]] = Scraper(config=ShopConfigurationDB(**s))


# async def initialise():
#     global scrapers
#     """Reads scraper information from /etc and populates the database with shop configs."""
#
#     with open(settings.SHOPS_YAML_PATH) as fileobj:
#         shopsconfig = yaml.safe_load_all(fileobj.read())
#
#     global scrapers
#     for config in shopsconfig:
#         shop = await shop_crud.read_by_name(config["name"])
#         if not shop:
#             logger.info(f"Shop not found adding: {config['name']}")
#             shop = await shop_crud.create(ShopConfigurationSchema(**config))
#
#         scrapers[shop["id"]] = Scraper(config=ShopConfigurationDB(**shop))
