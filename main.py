from typing import Final
from uuid import UUID, uuid4

from dotenv import load_dotenv
from flashbots import flashbot
from flashbots.types import FlashbotsBundleTx, HexStr
from pick import pick
from web3 import HTTPProvider, Web3
from web3.exceptions import TransactionNotFound


def main() -> None:
    option, _ = pick(constants.PICK_MENU_OPTIONS, constants.PICK_MENU_TITLE)
    match option:
        case "Yes":
            print("Continuing")
        case "No":
            print("Please edit the .env file to include the proper private keys and addresses")  # fmt: skip
            exit()

    # Create Web3 provider and inject flashbots module
    w3: Web3 = Web3(
        HTTPProvider(
            constants.HTTP_PROVIDER_MAINNET
            if constants.CHAIN_ID == 1
            else constants.HTTP_PROVIDER_GOERLI
        )
    )
    flashbot(
        w3,
        constants.ETH_BUNDLE_SUBMITTER,
        (
            constants.HTTP_FLASHBOTS_URI_MAINNET
            if constants.CHAIN_ID == 1
            else constants.HTTP_FLASHBOTS_URI_GOERLI
        ),
    )

    # Construct tx bundle from ./bundle/bundle.py
    print("Constructing bundle")
    BUNDLE: Final[list[FlashbotsBundleTx]] = [
        {"transaction": tx, "signer": constants.ETH_GASSER_ACCOUNT_SIGNER}
        for tx in gasser_wallet_txs
    ] + [
        {"transaction": tx, "signer": constants.ETH_COMPROMISED_ACCOUNT_SIGNER}
        for tx in compromised_wallet_txs
    ]

    # Attempt to mine bundle
    while True:
        current_block: int = w3.eth.block_number
        target_block: int = current_block + 1
        print(f"Simulating bundle on block {current_block}")
        try:
            w3.flashbots.simulate(BUNDLE, current_block)
            print("Simulation successful")
        except Exception as error:
            print(f"Simulation failed, {error=}")
            return

        replacement_uuid: UUID = str(uuid4())
        print(f"Sending bundle targeting block {target_block}")
        print(f"{replacement_uuid=}")

        send_result = w3.flashbots.send_bundle(
            BUNDLE,
            target_block_number=target_block,
            opts={"replacementUuid": replacement_uuid},
        )
        bundle_hash: HexStr = w3.toHex(send_result.bundle_hash())
        print(f"{bundle_hash=}")

        send_result.wait()
        try:
            receipts = send_result.receipts()
            print(f"Bundle was successfully mined in block {receipts[0].blockNumber}")
            break
        except TransactionNotFound:
            print(f"Bundle was not found in block {target_block}, canceling")
            cancel_res = w3.flashbots.cancel_bundles(replacement_uuid)
            print(f"{cancel_res=}")


if __name__ == "__main__":
    load_dotenv()
    import utils.constants as constants
    from bundle.bundle import compromised_wallet_txs, gasser_wallet_txs

    main()
