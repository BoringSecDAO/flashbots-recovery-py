from web3 import HTTPProvider, Web3
from web3.types import TxParams

import utils.abi as abi
import utils.constants as constants

w3: Web3 = Web3(
    HTTPProvider(
        constants.HTTP_PROVIDER_MAINNET
        if constants.CHAIN_ID == 1
        else constants.HTTP_PROVIDER_GOERLI
    )
)

"""
    ! Build your bundle here 
    -----------------------
    - `gasser_wallet_txs` is a simple ETH transfer TX from your wallet that will be providing gas. Generally,
    nothing here will need to be changed besides the `value` field (how much ETH you will be sending). However,
    it is possible to add more TXs executed by the gasser wallet.

    - `compromised_wallet_txs` is a list of TXs that you want to execute, e.g., transfer an NFT, unstake and
    transfer two different ERC20 tokens, and claim an ERC20 token airdrop and transfer the tokens. The TXs in
    this list will completely depend on what you need/want to rescue. Common and generic ABIs are provided
    under `abi`, utils.abi, (ERC721, ERC1155, ERC20, and a generic mutli transfer contract). If custom ABIs
    are required, put them in `./utils/abi.py`, and make sure the they follow pythonic notation.
"""

# We only need a single tx from the gas wallet
gasser_wallet_txs: list[TxParams] = [
    {
        "to": constants.ETH_COMPROMISED_ACCOUNT_SIGNER.address,
        "value": Web3.toWei(0.01, "ether"),
        "gas": constants.SEND_ETH_GAS_LIMIT,
        "maxFeePerGas": constants.MAX_FEE,
        "maxPriorityFeePerGas": constants.MAX_TIP,
        "nonce": w3.eth.get_transaction_count(
            constants.ETH_GASSER_ACCOUNT_SIGNER.address
        ),
        "chainId": constants.CHAIN_ID,
        "data": "",
        "type": 2,
    },
]

compromised_wallet_txs: list[TxParams] = [
    {},
]
