import json
import logging

import aiohttp

from bovine.utils.parse import parse_fediverse_handle

from .consts import BOVINE_CLIENT_NAME

logger = logging.getLogger(__name__)


async def lookup_with_webfinger(
    session: aiohttp.ClientSession, webfinger_url: str, params: dict
):
    async with session.get(
        webfinger_url, params=params, headers={"user-agent": BOVINE_CLIENT_NAME}
    ) as response:
        if response.status != 200:
            logger.warn(f"{params['resource']} not found using webfinger")
            return None
        text = await response.text()
        data = json.loads(text)

        if "links" not in data:
            return None

        links = data["links"]
        for entry in links:
            if "rel" in entry and entry["rel"] == "self":
                return entry["href"]

    return None


async def lookup_account_with_webfinger(
    session: aiohttp.ClientSession, fediverse_handle: str
) -> str | None:
    username, domain = parse_fediverse_handle(fediverse_handle)

    webfinger_url = f"https://{domain}/.well-known/webfinger"
    params = {"resource": f"acct:{username}@{domain}"}

    return await lookup_with_webfinger(session, webfinger_url, params)


async def lookup_did_with_webfinger(
    session: aiohttp.ClientSession, domain: str, did: str
) -> str | None:
    webfinger_url = f"https://{domain}/.well-known/webfinger"
    params = {"resource": did}

    return await lookup_with_webfinger(session, webfinger_url, params)
