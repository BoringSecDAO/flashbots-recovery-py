from os import getenv
from typing import Final

from eth_account.account import Account
from eth_account.signers.local import LocalAccount

# fmt: off
CHAIN_ID: Final[int] = 1
SEND_ETH_GAS_LIMIT: Final[int] = 21_000
HTTP_PROVIDER_MAINNET: Final[str] = f"https://eth-mainnet.g.alchemy.com/v2/{getenv('ALCHEMY_API_KEY')}"
HTTP_PROVIDER_GOERLI: Final[str] = f"https://eth-goerli.g.alchemy.com/v2/{getenv('ALCHEMY_API_KEY')}"
HTTP_FLASHBOTS_URI_MAINNET: Final[str] = "https://relay.flashbots.net"
HTTP_FLASHBOTS_URI_GOERLI: Final[str] = "https://relay-goerli.flashbots.net"

# Gas fees, denominated in Gwei
MAX_FEE: Final[int] = 15
MAX_TIP: Final[int] = 15

# Account signers
ETH_COMPROMISED_ACCOUNT_SIGNER: Final[LocalAccount] = Account.from_key(getenv("ETH_COMPROMISED_PRIVATE_KEY"))
ETH_GASSER_ACCOUNT_SIGNER: Final[LocalAccount] = Account.from_key(getenv("ETH_GASSER_PRIVATE_KEY"))

# Known, safe addresses
ETH_SAFE_ADDRESS: Final[str] = getenv("ETH_SAFE_ADDRESS")
ETH_MULTI_TRANSFER_CONTRACT: Final[str] = getenv("ETH_MULTI_TRANSFER_CONTRACT")

# The following account is solely used to submit bundles to the Flashbots relay
# No real funds will be held in this account, so we don't care if the private key is known
# DO NOT USE THIS ACCOUNT - DO NOT SEND FUNDS TO THIS ACCOUNT - DO NOT SEND ANYONE YOUR ACTUAL PRIVATE KEY(S)
ETH_BUNDLE_SUBMITTER_PRIVATE_KEY: Final[str] = "0xaade5309cd0ba010c0b0f45c1035727cd88089d73416e8e59f302ba91271e468"
ETH_BUNDLE_SUBMITTER: Final[LocalAccount] = Account.from_key(ETH_BUNDLE_SUBMITTER_PRIVATE_KEY)

# Pick menu options and title
PICK_MENU_OPTIONS: Final[list[str]] = ["Yes", "No"]
PICK_MENU_TITLE: Final[str] = f"Are the following addresses correct (use the arrows keys to move and enter to select)?\n- Compromised Wallet: {ETH_COMPROMISED_ACCOUNT_SIGNER.address}\n- Gas Provider Wallet: {ETH_GASSER_ACCOUNT_SIGNER.address}\n- Safe Recovery Wallet: {ETH_SAFE_ADDRESS}"
