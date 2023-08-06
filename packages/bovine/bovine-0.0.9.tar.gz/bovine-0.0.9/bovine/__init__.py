import aiohttp
import tomli

from .activitypub.actor import ActivityPubActor


class BovineActor(ActivityPubActor):
    def __init__(self, config):
        self.config = config
        super().__init__()

    async def init(self, session=None):
        self.session = session
        if session is None:
            self.session = aiohttp.ClientSession()

        if self._has_moo_auth():
            await self.with_host_and_ed25519_private_key(
                self.config["host"], self.config["private_key"], session=self.session
            )
        elif self._has_http_signature():
            self.actor_id = self.config["account_url"]
            self.with_http_signature(
                self.config["public_key_url"],
                self.config["private_key"],
                session=self.session,
            )
        else:
            raise Exception("No known authorization method available")

        await self.load()

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, *args):
        await self.session.close()

    def _has_http_signature(self):
        return self._has_keys(["account_url", "public_key_url", "private_key"])

    def _has_moo_auth(self):
        return self._has_keys(["host", "private_key"])

    def _has_keys(self, key_list):
        for key in key_list:
            if key not in self.config:
                return False

        return True

    @staticmethod
    def from_file(config_file):
        with open(config_file, "rb") as fp:
            config = tomli.load(fp)

        return BovineActor(config)
