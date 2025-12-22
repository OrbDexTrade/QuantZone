from decimal import Decimal
from typing import Optional

from pydantic import Field, SecretStr
from pydantic.class_validators import validator

from hummingbot.client.config.config_data_types import BaseConnectorConfigMap, ClientFieldData
from hummingbot.core.data_type.trade_fee import TradeFeeSchema

# Maker rebates(-0.02%) are paid out continuously on each trade directly to the trading wallet.(https://orbdex.gitbook.io/orbdex-docs/trading/fees)
DEFAULT_FEES = TradeFeeSchema(
    maker_percent_fee_decimal=Decimal("-0.00005"),
    taker_percent_fee_decimal=Decimal("0.0003"),
    buy_percent_fee_deducted_from_returns=True
)

CENTRALIZED = True
EXAMPLE_PAIR = "BTC-USD"
BROKER_ID = "HBOT"


def validate_bool(value: str) -> Optional[str]:
    """
    Permissively interpret a string as a boolean
    """
    valid_values = ('true', 'yes', 'y', 'false', 'no', 'n')
    if value.lower() not in valid_values:
        return f"Invalid value, please choose value from {valid_values}"


class OrbDexPerpetualConfigMap(BaseConnectorConfigMap):
    connector: str = Field(default="orbdex_perpetual", client_data=None)
    orbdex_perpetual_l1_address: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your L1 Address",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    orbdex_perpetual_is_testnet: bool = Field(
        default="testing this", 
        client_data=ClientFieldData(
            prompt=lambda cm: "is_testnet",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    orbdex_perpetual_l1_private_key: SecretStr = Field(
        default=None,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your L1 private key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    orbdex_perpetual_l2_private_key: SecretStr = Field(
        default=None,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your L2 private key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )


KEYS = OrbDexPerpetualConfigMap.construct()



OTHER_DOMAINS = ["orbdex_perpetual_testnet"]
OTHER_DOMAINS_PARAMETER = {
    "orbdex_perpetual_testnet": "orbdex_perpetual_testnet",
}
OTHER_DOMAINS_EXAMPLE_PAIR = {
    "orbdex_perpetual_testnet": EXAMPLE_PAIR,
}
OTHER_DOMAINS_DEFAULT_FEES = {
    "orbdex_perpetual_testnet": [0, 0.025],
}

class OrbDexPerpetualTestnetConfigMap(BaseConnectorConfigMap):
    connector: str = Field(default="orbdex_perpetual_testnet", client_data=None)
    orbdex_perpetual_l1_address: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your L1 Address",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    orbdex_perpetual_is_testnet: bool = Field(
        default=True,
        client_data=ClientFieldData(is_connect_key=True)
    )
    
    orbdex_perpetual_l1_private_key: SecretStr = Field(
        default=None,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your L1 private key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    orbdex_perpetual_l2_private_key: SecretStr = Field(
        default=None,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your L2 private key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )

    class Config:
        title = "orbdex_perpetual"


OTHER_DOMAINS_KEYS = {
    "orbdex_perpetual_testnet": OrbDexPerpetualTestnetConfigMap.construct(),
}
