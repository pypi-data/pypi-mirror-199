# standard imports
import os
import unittest
import json
import logging

# external imports
from chainlib.eth.unittest.ethtester import EthTesterCase
from chainlib.connection import RPCConnection
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.address import to_checksum_address
from chainlib.eth.tx import (
        receipt,
        transaction,
        TxFormat,
        )
from chainlib.eth.contract import (
        abi_decode_single,
        ABIContractType,
        )
from chainlib.eth.block import (
        block_latest,
        block_by_number,
        )

# local imports
from eth_accounts_index.registry import AccountRegistry
from eth_accounts_index import AccountsIndex

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

testdir = os.path.dirname(__file__)


class TestNonceOracle:

    def __init__(self, address, default_value=0):
        self.nonce = default_value


    def next_nonce(self):
        nonce = self.nonce
        self.nonce += 1
        return nonce


class Test(EthTesterCase):

    def setUp(self):
        super(Test, self).setUp()
        nonce_oracle = TestNonceOracle(self.accounts[0])
        c = AccountRegistry(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.constructor(self.accounts[0])
        self.conn = RPCConnection.connect(self.chain_spec, 'default')
        r = self.conn.do(o)
        logg.debug(f'published with hash {r}')

        o = receipt(r)
        r = self.conn.do(o)
        self.address = to_checksum_address(r['contract_address'])

        (tx_hash, o) = c.add_writer(self.address, self.accounts[0], self.accounts[0])
        r = self.conn.do(o)

        o = receipt(r)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)


    def test_1_count(self):
        #o = self.o.count(self.address, sender_address=self.accounts[0])
        c = AccountsIndex(self.chain_spec)
        o = c.entry_count(self.address, sender_address=self.accounts[0])
        r = self.conn.do(o)
        r = abi_decode_single(ABIContractType.UINT256, r)
        self.assertEqual(r, 0)


    def test_2_add(self):
        b = os.urandom(20)
        a = to_checksum_address(b.hex())
        b = os.urandom(20)
        b = to_checksum_address(b.hex())

        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        c = AccountsIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.add(self.address, self.accounts[0], a)
        self.conn.do(o)
        o = receipt(tx_hash)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        self.helper.mine_block()
        o = c.have(self.address, a, sender_address=self.accounts[0])
        r = self.conn.do(o)
        self.assertEqual(int(r, 16), 1)

        o = c.have(self.address, b, sender_address=self.accounts[0])
        r = self.conn.do(o)
        self.assertEqual(int(r, 16), 0)


    def test_3_add_rlpsigned(self):
        b = os.urandom(20)
        a = to_checksum_address(b.hex())

        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        c = AccountsIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.add(self.address, self.accounts[0], a) #, tx_format=TxFormat.RLP_SIGNED)
        r = self.conn.do(o)
        self.assertEqual(tx_hash, r)
        logg.debug('o {}'.format(o))


    def test_4_indices(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        c = AccountsIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)

        o = c.entry_count(self.address, sender_address=self.accounts[0])
        r = self.conn.do(o)
        count = c.parse_entry_count(r)
        self.assertEqual(count, 0)

        b = os.urandom(20)
        a = to_checksum_address(b.hex())
        (tx_hash, o) = c.add(self.address, self.accounts[0], a)
        r = self.conn.do(o)

        b = os.urandom(20)
        aa = to_checksum_address(b.hex())
        (tx_hash, o) = c.add(self.address, self.accounts[0], aa)
        r = self.conn.do(o)

        o = c.entry_count(self.address, sender_address=self.accounts[0])
        r = self.conn.do(o)
        count = c.parse_entry_count(r)
        self.assertEqual(count, 2)


    def test_5_deactivate(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        c = AccountsIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)

        b = os.urandom(20)
        a = to_checksum_address(b.hex())
        (tx_hash, o) = c.add(self.address, self.accounts[0], a)
        r = self.conn.do(o)

        o = c.entry_count(self.address, sender_address=self.accounts[0])
        r = self.conn.do(o)
        count = c.parse_entry_count(r)
        self.assertEqual(count, 1)

        b = os.urandom(20)
        a = to_checksum_address(b.hex())
        (tx_hash, o) = c.add(self.address, self.accounts[0], a)
        r = self.conn.do(o)

        o = c.entry_count(self.address, sender_address=self.accounts[0])
        r = self.conn.do(o)
        count = c.parse_entry_count(r)
        self.assertEqual(count, 2)

        (tx_hash, o) = c.deactivate(self.address, self.accounts[0], a)
        r = self.conn.do(o)
        o = receipt(r)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        o = c.entry_count(self.address, sender_address=self.accounts[0])
        r = self.conn.do(o)
        count = c.parse_entry_count(r)
        self.assertEqual(count, 2)

        o = c.have(self.address, a, sender_address=self.accounts[0])
        r = self.conn.do(o)
        self.assertEqual(int(r, 16), 1)

        o = c.is_active(self.address, a, sender_address=self.accounts[0])
        r = self.conn.do(o)
        self.assertEqual(int(r, 16), 0)

        (tx_hash, o) = c.activate(self.address, self.accounts[0], a)
        r = self.conn.do(o)
        o = receipt(r)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        o = c.have(self.address, a, sender_address=self.accounts[0])
        r = self.conn.do(o)
        self.assertEqual(int(r, 16), 1)

        o = c.is_active(self.address, a, sender_address=self.accounts[0])
        r = self.conn.do(o)
        self.assertEqual(int(r, 16), 1)


    def test_6_remove(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        c = AccountsIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)

        b = os.urandom(20)
        a = to_checksum_address(b.hex())
        (tx_hash, o) = c.add(self.address, self.accounts[0], a)
        r = self.conn.do(o)

        o = c.entry_count(self.address, sender_address=self.accounts[0])
        r = self.conn.do(o)
        self.assertEqual(int(r, 16), 1)

        (tx_hash, o) = c.remove(self.address, self.accounts[0], a)
        r = self.conn.do(o)
        o = receipt(r)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        o = c.entry_count(self.address, sender_address=self.accounts[0])
        r = self.conn.do(o)
        self.assertEqual(int(r, 16), 0)

        addrs = []
        for i in range(8):
            b = os.urandom(20)
            addrs.append(to_checksum_address(b.hex()))
            (tx_hash, o) = c.add(self.address, self.accounts[0], addrs[i])
            r = self.conn.do(o)
            o = receipt(tx_hash)
            r = self.conn.do(o)
            self.assertEqual(r['status'], 1)

        o = c.entry_count(self.address, sender_address=self.accounts[0])
        r = self.conn.do(o)
        self.assertEqual(int(r, 16), 8)

        (tx_hash, o) = c.remove(self.address, self.accounts[0], addrs[4])
        r = self.conn.do(o)
        o = receipt(r)
        r = self.conn.do(o)
        self.assertEqual(r['status'], 1)

        r = []
        for i in range(7):
            o = c.entry(self.address, i, sender_address=self.accounts[0])
            r.append(self.conn.do(o))

        self.assertEqual(len(r), 7)
        self.assertNotIn(addrs[4], r)


    def test_7_time(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.conn)
        c = AccountsIndex(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)

        b = os.urandom(20)
        a = to_checksum_address(b.hex())
        (tx_hash, o) = c.add(self.address, self.accounts[0], a)
        self.conn.do(o)

        o = block_latest()
        r = self.conn.do(o)
        o = block_by_number(r)
        r = self.conn.do(o)
        t = r['timestamp']

        o = c.time(self.address, a, sender_address=self.accounts[0])
        r = self.conn.do(o)
        self.assertEqual(t, int(r, 16))


if __name__ == '__main__':
    unittest.main()
