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
ERC20_CONTRACT = w3.eth.contract(address=NULL_ADDRESS, abi=abi.ERC_20_ABI)

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
    # Withdraw 1,000 APE tokens and unstake MAYC #1000 from ApeCoin Staking
    {
        "to": "0x5954ab967bc958940b7eb73ee84797dc8a2afbb9",
        "value": Web3.toWei(0, "ether"),
        "gas": 250_000,
        "maxFeePerGas": constants.MAX_FEE,
        "maxPriorityFeePerGas": constants.MAX_TIP,
        "nonce": w3.eth.get_transaction_count(
            constants.ETH_COMPROMISED_ACCOUNT_SIGNER.address
        ),
        "chainId": constants.CHAIN_ID,
        "data": "0xc63389c30000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000003e800000000000000000000000000000000000000000000003635c9adc5dea00000",
        "type": 2,
    },
    # Transfer 1,000 APE token
    {
        "to": "0xd9a442856c234a39a81a089c06451ebaa4306a72",
        "value": Web3.toWei(0, "ether"),
        "gas": 100_000,
        "maxFeePerGas": constants.MAX_FEE,
        "maxPriorityFeePerGas": constants.MAX_TIP,
        "nonce": w3.eth.get_transaction_count(
            constants.ETH_COMPROMISED_ACCOUNT_SIGNER.address
        ) + 1,
        "chainId": constants.CHAIN_ID,
        "data": ERC20_CONTRACT.encodeABI(
            "transfer",
            args=[
                constants.ETH_SAFE_ADDRESS,  # to
                1_000_000_000_000_000_000_000,  # amount (18 decimals)
            ],
        ),
        "type": 2,
    },
]
