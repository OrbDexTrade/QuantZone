import os
from typing import Optional

from orbdex_py import OrbDex
from orbdex_py.account.account import OrbDexAccount
from orbdex_py.api.api_client import OrbDexApiClient
from orbdex_py.environment import PROD, TESTNET, Environment
from hummingbot.core.web_assistant.auth import AuthBase
from hummingbot.core.web_assistant.connections.data_types import RESTRequest, WSRequest


class OrbDexPerpetualAuth(AuthBase):
    """
    Auth class required by OrbDex Perpetual API
    """
    def __init__(
        self,
        orbdex_perpetual_l1_address: str,
        orbdex_perpetual_is_testnet: bool,
        orbdex_perpetual_l1_private_key: Optional[str] = None,
        orbdex_perpetual_l2_private_key: Optional[str] = None
    ):
        self._orbdex_perpetual_l1_address = orbdex_perpetual_l1_address
        self._orbdex_perpetual_chain = TESTNET if orbdex_perpetual_is_testnet else PROD
        self._orbdex_perpetual_l1_private_key = orbdex_perpetual_l1_private_key
        self._orbdex_perpetual_l2_private_key = orbdex_perpetual_l2_private_key

        self._orbdex_account: OrbDexAccount = None
        self._rest_api_client: OrbDexApiClient = None

    @property
    def orbdex_account(self):
        if self._orbdex_account is None:
            self.orbdex_rest_client
        return self._orbdex_account

    @property
    def orbdex_rest_client(self):
        if self._rest_api_client is None:

            env = self._orbdex_perpetual_chain

            self._rest_api_client = OrbDexApiClient(
                env=env, 
                logger=None
            )
            self.config = self._rest_api_client.fetch_system_config()
            self._orbdex_account = OrbDexAccount(    
                config=self.config,
                l1_address=self._orbdex_perpetual_l1_address, 
                l1_private_key=self._orbdex_perpetual_l1_private_key,
                l2_private_key=self._orbdex_perpetual_l2_private_key
            )

            self._rest_api_client.init_account(self._orbdex_account)
        return self._rest_api_client

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        self.orbdex_rest_client._validate_auth()

        headers = self.orbdex_rest_client.client.headers

        if request.headers is not None:
            headers.update(request.headers)

        request.headers = headers
        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        return request
