import json
from typing import Any

import requests


class Web3RPC:
    def __init__(self, url: str, max_batch_size: int = 100, debug: bool = False):
        self.url = url
        self._id = 0
        self.errors = []
        self.debug = debug
        self.max_batch_size = max_batch_size

    def batch_raw_call(self, methods: list[str], paramss: list[Any]) -> list:
        """Send batched raw RPC calls."""

        self._validate_input(methods, paramss)
        rpc_commands = self._prepare_rpcs(methods, paramss)

        for batch in self._batch_it(rpc_commands):
            response = self._rpc_call(self.url, batch)
            yield self._get_valid_responses(response, batch)

    def reset_errors(self):
        self.errors = []

    def _prepare_rpcs(self, methods: list[str], paramss: list[Any]) -> list[dict]:
        """Prepare a list of RPC commands."""
        return [
            self._prepare_rpc(method=method, params=params)
            for method, params in zip(methods, paramss)
        ]

    def _prepare_rpc(self, method: str, params: list[Any]) -> dict:
        return {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
            "params": params,
        }

    def _next_id(self):
        self._id += 1
        return self._id

    def _batch_it(self, rpc_commands: list[dict]):
        """Yield batches of RPC commands."""
        for i in range(0, len(rpc_commands), self.max_batch_size):
            yield rpc_commands[i : i + self.max_batch_size]  # noqa: E203

    def _rpc_call(self, url: str, payload: list) -> list:
        """Send an RPC call to the specified URL with the given payload."""
        self._log(f"curl -XPOST {url} --data '{json.dumps(payload)}'")
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return response.json()

        raise Exception(f"Response Error: {response.status_code} {response.text}")

    def _get_valid_responses(self, response, rpc_commands) -> list[dict]:
        valids = []
        for i in range(len(response)):
            row = response[i]
            if "error" in row:
                self._log(
                    f'Error: {row["error"]} with command: {rpc_commands[i]}'  # noqa: E501
                )
                self.errors.append(row)
            else:
                valids.append(row)

        return valids

    def _log(self, message: str):
        if self.debug:
            print(message)

    @staticmethod
    def _validate_input(methods, paramss):
        if len(methods) != len(paramss):
            raise ValueError(
                f"Number of methods {len(methods)} does not match number of params {len(paramss)}"  # noqa: E501
            )
