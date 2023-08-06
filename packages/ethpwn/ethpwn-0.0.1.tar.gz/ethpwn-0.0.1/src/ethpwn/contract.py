from collections import defaultdict
from contextlib import contextmanager
import json
import os
from time import sleep
from typing import Any, Dict, Generator, List, Tuple, Union
from hexbytes import HexBytes
from solcx import compile_source, compile_files
from web3.types import TxReceipt
from web3.contract import Contract, ContractFunction
import solcx

from .json_utils import json_dump, json_load

from .config.wallets import get_wallet_by_address, Wallet
from .config import get_logged_deployed_contracts_dir
from .transactions import transact
from .global_context import context
from .hashes import lookup_signature_hash, register_signature_hash, signature_hash

def log_deployed_contract(metadata, tx_hash: HexBytes, tx_receipt: TxReceipt):
    address = tx_receipt['contractAddress']
    deployed_contracts_path = get_logged_deployed_contracts_dir()
    os.makedirs(deployed_contracts_path, exist_ok=True)
    deployed_contracts_path += f"{address}.json"
    with open(deployed_contracts_path, 'w') as f:
        json_dump({
            'from_wallet': get_wallet_by_address(tx_receipt['from']).to_json_dict(),
            'tx_hash': tx_hash,
            'tx_receipt': tx_receipt,
            'metadata': metadata.to_json_dict(),
        }, f)

def all_previously_deployed_contracts():
    deployed_contracts_path = get_logged_deployed_contracts_dir()
    for file in os.listdir(deployed_contracts_path):
        if file.endswith('.json'):
            with open(deployed_contracts_path + file, 'r') as f:
                data = json.load(f)
                wallet = Wallet.from_json_dict(data['from_wallet'])
                tx_hash = HexBytes.fromhex(data['tx_hash'])
                tx_receipt = TxReceipt(data['tx_receipt'])
                metadata = ContractMetadata.from_json_dict(data['metadata'])
                yield wallet, tx_hash, tx_receipt, metadata

def all_previously_deployed_contracts_with_balance_remaining():
    for wallet, tx_hash, tx_receipt, metadata in all_previously_deployed_contracts():
        balance = context.w3.eth.get_balance(tx_receipt.contractAddress)
        if balance > 0:
            yield wallet, tx_hash, tx_receipt, metadata, balance

TYPED_CONTRACTS: Dict[str, 'ContractMetadata'] = {}

def register_typed_contract(address: str, contract_metadata: 'ContractMetadata'):
    TYPED_CONTRACTS[address] = contract_metadata

def get_typed_contract(address: str):
    return TYPED_CONTRACTS.get(address, None)

def decode_function_input(address, input, guess=False):
    if address in TYPED_CONTRACTS:
        metadata = TYPED_CONTRACTS[address]
        return metadata, *metadata.decode_function_input(input)
    elif guess:
        for name, metadata in CONTRACT_METADATA.contract_info[''].items():
            try:
                return metadata, *metadata.decode_function_input(input)
            except ValueError as e:
                continue

    # worst case: We don't know what this contract is, so we just at least try to decode the function selector
    selector = input.hex()[2:10]
    if len(selector) == 8:
        func_signature = lookup_signature_hash(selector)
        if func_signature is not None:
            return None, func_signature, [input[4:]]

    return None

class ContractMetadata:
    def __init__(self, **kwargs) -> None:
        self.file_name = kwargs.pop('file_name', None)
        self.contract_name = kwargs.pop('contract_name', None)
        self.json_dict = kwargs

    def to_json_dict(self):
        # dump file_name, contract_name, and json_dict
        return {
            'file_name': self.file_name,
            'contract_name': self.contract_name,
            **self.json_dict
        }

    def from_json_dict(d):
        return ContractMetadata(**d)

    def __getattr__(self, __name: str) -> Any:
        if __name in self.json_dict:
            return self.json_dict[__name]
        else:
            raise AttributeError(f"ContractMetadata has no attribute {__name}")

    def deploy(self, *constructor_args, log=True, **tx_extras) -> Tuple[HexBytes, Contract]:
        tx_hash, tx_receipt = transact(
            context.w3.eth.contract(
                abi=self.abi,
                bytecode=self.bin
            ).constructor(*constructor_args),
            **tx_extras
        )

        if log:
            log_deployed_contract(self, tx_hash, tx_receipt)

        address = tx_receipt['contractAddress']
        register_typed_contract(address, self)
        return tx_hash, self.get_contract_at(address)

    @contextmanager
    def deploy_destructible(self, *constructor_args, **tx_extras):
        tx_hash, contract = self.deploy(*constructor_args, log=False, **tx_extras)
        exception = None
        try:
            yield tx_hash, contract
        except Exception as e:
            exception = e
            raise
        finally:
            sleep(2)
            if exception:
                context.logger.info(f"Encountered exception: {exception}")
            context.logger.info(f"Destroying contract {contract.address} to get funds back!")
            transact(contract.functions.destroy(), from_addr=tx_extras.get('from_addr', None))

    def get_contract_at(self, addr) -> Contract:
        register_typed_contract(addr, self)
        return context.w3.eth.contract(
            address=addr,
            abi=self.abi
        )

    def decode_function_input(self, data):
        c = context.w3.eth.contract(abi=self.abi)
        return c.decode_function_input(data)


class ContractMetadataRegistry:
    def __init__(self) -> None:
        self.contract_info: Dict[str, Dict[str, ContractMetadata]] = defaultdict(dict)
        self.default_import_remappings: Dict[str, str] = {
            "exploit_templates": os.path.dirname(os.path.realpath(__file__)) + "/exploit_templates",
        }

    def add_default_import_remappings(self, remappings: Dict[str, str]):
        self.default_import_remappings.update(remappings)

    def get_output_values(self):
        output_values = ['abi','bin','bin-runtime','asm','hashes','metadata','srcmap','srcmap-runtime']
        if solcx.get_solc_version().minor >= 6:
            output_values.append('storage-layout')
        return output_values

    def find_pragma_line(self, content: str):
        for line in content.splitlines():
            if line.strip().startswith('pragma solidity'):
                return line

    def get_pragma_lines(self, files: List[str]):
        pragma_lines = set()
        for file in files:
            with open(file, 'r') as f:
                solidity_pragma_line = self.find_pragma_line(f.read())
                if solidity_pragma_line is not None:
                    pragma_lines.add(solidity_pragma_line)
        return list(pragma_lines)

    def configure_solcx_for_pragma(self, pragma_line: str):
        if pragma_line is None:
            return

        solcx.install_solc_pragma(pragma_line)
        solcx.set_solc_version_pragma(pragma_line)

    def get_import_remappings(self, **kwargs):
        import_remappings = {} if kwargs.get('no_default_import_remappings', False) else self.default_import_remappings.copy()
        if 'import_remappings' in kwargs:
            import_remappings.update(kwargs.pop('import_remappings'))
        return import_remappings

    def register_contract(self, contract_name, contract_data, rename_stdin_to=None):
        file, name = contract_name.split(':')
        if rename_stdin_to is not None and file == '<stdin>':
            file = rename_stdin_to
        meta = ContractMetadata(file_name=file, contract_name=name, **contract_data)
        self.contract_info[file][name] = meta
        self.contract_info[''][name] = meta

        for signature, hash in meta.hashes.items():
            register_signature_hash(signature, hash)

    def add_solidity_source(self, source: str, file_name: str, **kwargs):

        self.configure_solcx_for_pragma(self.find_pragma_line(source))

        contracts = compile_source(
            source,
            import_remappings=self.get_import_remappings(**kwargs),
            output_values=self.get_output_values(),
            **kwargs
            )

        for contract_name, contract_data in contracts.items():
            self.register_contract(contract_name, contract_data, rename_stdin_to=file_name)


    def add_solidity_files(self, files: List[str], **kwargs):
        pragma_lines = self.get_pragma_lines(files)
        assert len(pragma_lines) <= 1, "Multiple solidity versions in files"
        self.configure_solcx_for_pragma(pragma_lines[0] if len(pragma_lines) == 1 else None)

        contracts = compile_files(
            files,
            import_remappings=self.get_import_remappings(**kwargs),
            output_values=self.get_output_values(),
            **kwargs
            )

        for contract_name, contract_data in contracts.items():
            self.register_contract(contract_name, contract_data)

    # make it so that metadata_registry['name'] returns the metadata for the contract of that name, and metadata_registry[('file', 'name')] returns the metadata for the contract of that name in that file
    def __getitem__(self, key: Union[str, Tuple[str, str]]) -> ContractMetadata:
        if isinstance(key, tuple):
            return self.contract_info[key[0]][key[1]]
        else:
            return self.contract_info[''][key]

    def all_contracts(self):
        for file_name, file_data in self.contract_info.items():
            for contract_name, contract_data in file_data.items():
                yield file_name, contract_name, contract_data

    # def save_to(self, path):
    #     import json
    #     for file_name, file_data in self.contract_info.items():
    #         with open(f'{path}/{file_name}.json', 'w') as f:
    #             for contract_name, contract_data in file_data.items():
    #                 withjson.dump(file_data, f,

CONTRACT_METADATA: ContractMetadataRegistry = ContractMetadataRegistry()
