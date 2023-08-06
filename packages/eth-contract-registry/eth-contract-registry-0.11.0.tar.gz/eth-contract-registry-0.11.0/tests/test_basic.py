# standard imports
import os
import unittest
import json
import logging
import hashlib

# external imports
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.eth.contract import (
        ABIContractEncoder,
        ABIContractType,
        )
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt
from giftable_erc20_token import GiftableToken
from hexathon import (
    add_0x,
    strip_0x,
    same as same_hex,
    )

# local imports
from eth_contract_registry.registry import ContractRegistry
from eth_contract_registry import Registry

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestContractRegistry(EthTesterCase):

    def setUp(self):
        super(TestContractRegistry, self).setUp()
        self.registry_ids = ['FOo', 'Bar', 'baz', 'XYZZY']

        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = ContractRegistry(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.constructor(self.accounts[0], self.registry_ids)
        self.rpc.do(o)
        o = receipt(tx_hash_hex)
        rcpt = self.rpc.do(o)
        self.assertEqual(rcpt['status'], 1)
        self.address = rcpt['contract_address'] 
        logg.info('registry published to ' + self.address)


    def test_retrieve(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = ContractRegistry(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash_hex, o) = c.set(self.address, self.accounts[0], 'FOO', self.address)
        r = self.rpc.do(o)
        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 0)

        (tx_hash_hex, o) = c.set(self.address, self.accounts[0], 'FOo', self.address)
        r = self.rpc.do(o)
        o = receipt(tx_hash_hex)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        c = ContractRegistry(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        o = c.address_of(self.address, 'FOo', sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertTrue(same_hex(strip_0x(r)[24:], self.address))


    def test_identifiers(self):
        c = Registry(self.chain_spec)

        o = c.identifier_count(self.address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        self.assertEqual(int(r, 16), 4)
            
        for i in range(4):
            o = c.identifier(self.address, i, sender_address=self.accounts[0])
            r = self.rpc.do(o)
            r = bytes.fromhex(strip_0x(r))
            r = r.strip(b'\x00')
            s = r.decode('utf-8')
            self.assertEqual(s, self.registry_ids[i])
    

if __name__ == '__main__':
    unittest.main()
