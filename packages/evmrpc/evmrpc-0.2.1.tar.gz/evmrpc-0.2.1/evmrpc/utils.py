from datetime import datetime
from typing import Any
from typing import cast

from eth_utils.abi import collapse_if_tuple
from web3.types import ABIFunction


def get_abi_output_types(abi: ABIFunction) -> list[str]:
    if abi["type"] == "fallback":
        return []
    else:
        return [collapse_if_tuple(cast(dict[str, Any], arg)) for arg in abi["outputs"]]


def get_abi_output_names(abi: ABIFunction) -> list[str]:
    if "outputs" not in abi and abi["type"] == "fallback":
        return []
    else:
        return [arg["name"] for arg in abi["outputs"]]


def hex_to_date(value: str) -> datetime:
    return datetime.fromtimestamp(int(value, 16))


def hex_to_int(value: str) -> int:
    return int(value, 16)


def parse_block_hex_field(obj: dict) -> dict:
    for key, value in obj.items():
        if key == "timestamp":
            obj[key] = hex_to_date(value)
        elif isinstance(value, list):
            obj[key] = [hex_to_date(v) for v in value]
        else:
            obj[key] = hex_to_int(value)
    return obj


def is_hex(value: str) -> bool:
    try:
        int(value, 16)
        return True
    except ValueError:
        return False


def is_int(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False
