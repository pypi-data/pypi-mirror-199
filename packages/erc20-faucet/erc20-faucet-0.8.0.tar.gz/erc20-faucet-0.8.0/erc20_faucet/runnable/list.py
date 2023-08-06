"""Query faucet store

.. moduleauthor:: Louis Holbrook <dev@holbrook.no>
.. pgp:: 0826EDA1702D1E87C6E2875121D2E7BB88C2A746 

"""

# standard imports
import sys
import os
import json
import argparse
import logging

# external imports
import chainlib.eth.cli
from chainlib.chain import ChainSpec
from chainlib.eth.connection import EthHTTPConnection
from chainlib.eth.tx import receipt
from chainlib.eth.constant import ZERO_CONTENT
from chainlib.error import JSONRPCException
from chainlib.eth.address import to_checksum_address
from hexathon import (
        add_0x,
        strip_0x,
        )

# local imports
from erc20_faucet import Faucet
from erc20_faucet.faucet import SingleShotFaucet

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()


arg_flags = chainlib.eth.cli.argflag_std_write | chainlib.eth.cli.Flag.EXEC
argparser = chainlib.eth.cli.ArgumentParser(arg_flags)
argparser.add_positional('address', required=False, type=str, help='Check only whether given address has been used')
args = argparser.parse_args()

extra_args = {
    'address': None,
        }
config = chainlib.eth.cli.Config.from_args(args, arg_flags, extra_args=extra_args, default_fee_limit=SingleShotFaucet.gas())

wallet = chainlib.eth.cli.Wallet()
wallet.from_config(config)

rpc = chainlib.eth.cli.Rpc(wallet=wallet)
conn = rpc.connect_by_config(config)

chain_spec = ChainSpec.from_chain_str(config.get('CHAIN_SPEC'))


def out_element(e, conn, w=sys.stdout):
    w.write(str(e[1]) + '\n')


def element(ifc, conn, faucet_address, address, w=sys.stdout):
    o = ifc.usable_for(faucet_address, address)
    r =  conn.do(o)
    usable = ifc.parse_usable_for(r)
    if usable:
        out_element((0, address), conn, w)


def main():
    faucet_address = to_checksum_address(config.get('_EXEC_ADDRESS'))
    if not config.true('_UNSAFE') and faucet_address != add_0x(config.get('_EXEC_ADDRESS')):
        raise ValueError('invalid checksum address for faucet')

    address = to_checksum_address(config.get('_EXEC_ADDRESS'))
    if not config.true('_UNSAFE') and address != add_0x(config.get('_EXEC_ADDRESS')):
        raise ValueError('invalid checksum address for faucet')


    c = Faucet(chain_spec)
    element(c, conn, faucet_address, address, w=sys.stdout)


if __name__ == '__main__':
    main()
