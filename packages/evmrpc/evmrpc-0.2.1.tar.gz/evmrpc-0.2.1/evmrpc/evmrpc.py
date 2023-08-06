from typing import Union

from web3 import Web3
from web3.contract import Contract

from evmrpc import Web3RPC, get_abi_output_types, get_abi_output_names


class EvmRPC(Web3RPC):
    def __init__(self, url: str, max_batch_size: int = 100, debug: bool = False):
        super().__init__(url, max_batch_size, debug)
        self.web3 = Web3()

    def batch_eth_call(
        self, contract_calls: list[Contract], block_numbers: list[Union[int, str]] = []
    ):
        if len(contract_calls) != len(block_numbers):
            raise Exception(
                f"Number of contracts {len(contract_calls)} does not match number of blocks {len(block_numbers)}"  # noqa: E501
            )

        rpc_commands = [
            self._prepare_rpc(
                method="eth_call",
                params=self.prepare_eth_call(contract, block),
            )
            for contract, block in zip(contract_calls, block_numbers)
        ]
        for batch in self._batch_it(rpc_commands):
            response = self._rpc_call(self.url, batch)
            valid_responses = self._get_valid_responses(response, batch)
            yield [
                self._decode_response(contract, row)
                for contract, row in zip(contract_calls, valid_responses)
            ]

    @staticmethod
    def prepare_eth_call(contract: Contract, block_number: int = None) -> list[dict]:
        return [
            {
                "from": "0x0000000000000000000000000000000000000000",
                "to": contract.address,
                "data": contract._encode_transaction_data(),
            },
            hex(block_number) if isinstance(block_number, int) else block_number,
        ]

    def _decode_response(self, contract: Contract, response):
        result = response["result"]

        if result == "0x":
            return "0x"
        output_types = get_abi_output_types(contract.abi)
        output_names = get_abi_output_names(contract.abi)
        _hex = result[2:]
        hex_string_byte_array = bytes.fromhex(_hex)
        decoded_output = self.web3.codec.decode(
            tuple(output_types), hex_string_byte_array
        )

        if len(decoded_output) == 1:
            return decoded_output[0]
        return {
            output_name: decoded_out
            for output_name, decoded_out in zip(output_names, decoded_output)
        }
