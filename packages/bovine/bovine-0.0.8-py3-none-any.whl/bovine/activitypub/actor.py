import json
import logging
from urllib.parse import urlparse

import aiohttp
import tomli

from bovine.clients.lookup_account import lookup_did_with_webfinger
from bovine.clients.moo_auth_client import MooAuthClient
from bovine.clients.signed_http_client import SignedHttpClient
from bovine.utils.crypto.did_key import private_key_to_did_key

from .activity_factory import ActivityFactory
from .collection_helper import CollectionHelper
from .object_factory import ObjectFactory

logger = logging.getLogger(__name__)


class ActivityPubActor:
    def __init__(self):
        self.actor_id = None
        self.client = None
        self.information = None
        self._activity_factory = None
        self._object_factory = None

    async def with_host_and_ed25519_private_key(self, host, private_key, session=None):
        if session is None:
            session = aiohttp.ClientSession()
        did_key = private_key_to_did_key(private_key)

        self.actor_id = await lookup_did_with_webfinger(session, host, did_key)

        self.client = MooAuthClient(session, did_key, private_key)

        # await self.load()

        return self

    def with_actor_id(self, actor_id):
        self.actor_id = actor_id
        return self

    def with_http_signature(self, public_key_url, private_key, session=None):
        if session is None:
            session = aiohttp.ClientSession()

        self.client = SignedHttpClient(session, public_key_url, private_key)

        return self

    async def load(self):
        if self.client is None:
            raise Exception("Client not set in ActivityPubActor")
        self.information = await self.get(self.actor_id)

        logger.debug("Retrieved information %s", self.information)

        if any(required not in self.information for required in ["inbox", "outbox"]):
            raise Exception("Retrieved incomplete actor data")

    async def send_to_outbox(self, data: dict):
        if self.information is None:
            await self.load()

        return await self.post(self.information["outbox"], data)

    async def post(self, target, data: dict):
        response = await self.client.post(target, json.dumps(data))
        response.raise_for_status()

        return response

    async def proxy_element(self, target):
        response = await self.client.post(
            self.information["endpoints"]["proxyUrl"],
            f"id={target}",
            content_type="application/x-www-form-urlencoded",
        )
        response.raise_for_status()
        return await response.json()

    async def get_ordered_collection(self, url, max_items=None):
        result = await self.client.get(url)
        result.raise_for_status()

        data = json.loads(await result.text())

        total_number_of_items = data["totalItems"]
        items = []

        if "orderedItems" in data:
            items = data["orderedItems"]

        if len(items) == total_number_of_items:
            return {"total_items": total_number_of_items, "items": items}

        if "first" in data:
            page_data = await self.get(data["first"])

            items = page_data["orderedItems"]

            while "next" in page_data and len(page_data["orderedItems"]) > 0:
                if max_items and len(items) > max_items:
                    return {"total_items": total_number_of_items, "items": items}

                page_data = await self.get(page_data["next"])

                items += page_data["orderedItems"]

        return {"total_items": total_number_of_items, "items": items}

    async def get(self, target):
        response = await self.client.get(target)
        response.raise_for_status()
        return json.loads(await response.text())

    async def event_source(self):
        if self.information is None:
            await self.load()

        event_source_url = self.information["endpoints"]["eventSource"]
        return self.client.event_source(event_source_url)

    @property
    def activity_factory(self):
        if self._activity_factory is None:
            self._activity_factory = ActivityFactory(self.information)
        return self._activity_factory

    @property
    def object_factory(self):
        if self._object_factory is None:
            self._object_factory = ObjectFactory(self.information)
        return self._object_factory

    @property
    def factories(self):
        return self.activity_factory, self.object_factory

    @property
    def host(self):
        return urlparse(self.actor_id).netloc

    async def inbox(self):
        inbox_collection = CollectionHelper(self.information["inbox"], self)
        await inbox_collection.refresh()
        return inbox_collection

    async def outbox(self):
        inbox_collection = CollectionHelper(self.information["outbox"], self)
        await inbox_collection.refresh()
        return inbox_collection

    @staticmethod
    def from_file(filename, session):
        with open(filename, "rb") as fp:
            data = tomli.load(fp)

        actor = ActivityPubActor(data["account_url"])
        actor.with_http_signature(
            data["public_key_url"], data["private_key"], session=session
        )

        return actor
