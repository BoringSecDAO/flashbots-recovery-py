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

NULL_ADDRESS: str = "0x0000000000000000000000000000000000000000"
ERC721_CONTRACT = w3.eth.contract(address=NULL_ADDRESS, abi=abi.ERC_721_ABI)

# We only need a single tx from the gas wallet
gasser_wallet_txs: list[dict[TxParams]] = [
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

compromised_wallet_txs: list[dict[TxParams]] = [
    # Transfer BAYC #1000
    {
        "to": w3.toChecksumAddress("0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"),
        "value": Web3.toWei(0, "ether"),
        "gas": 250_000,
        "maxFeePerGas": constants.MAX_FEE,
        "maxPriorityFeePerGas": constants.MAX_TIP,
        "nonce": w3.eth.get_transaction_count(
            constants.ETH_COMPROMISED_ACCOUNT_SIGNER.address
        ),
        "chainId": constants.CHAIN_ID,
        "data": ERC721_CONTRACT.encodeABI(
            "safeTransferFrom",
            args=[
                constants.ETH_COMPROMISED_ACCOUNT_SIGNER.address,  # from
                constants.ETH_SAFE_ADDRESS,  # to
                1_000,  # tokenId
            ],
        ),
        "type": 2,
    },
]
