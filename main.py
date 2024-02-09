from typing import Final
from uuid import uuid4

from dotenv import load_dotenv
from flashbots import flashbot
from pick import pick
from web3 import HTTPProvider, Web3
from web3.exceptions import TransactionNotFound

from bundle.bundle import compromised_wallet_txs, gasser_wallet_txs


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
    BUNDLE: Final[list[dict]] = [
        {"signer": constants.ETH_GASSER_ACCOUNT_SIGNER, "transaction": tx}
        for tx in gasser_wallet_txs
    ] + [
        {"signer": constants.ETH_COMPROMISED_ACCOUNT_SIGNER, "transaction": tx}
        for tx in compromised_wallet_txs
    ]

    # Attempt to mine bundle
    while True:
        current_block: int = w3.eth.block_number
        print(f"Simulating bundle on block {current_block}")
        try:
            w3.flashbots.simulate(BUNDLE, current_block)
            print("Simulation successful")
        except Exception as error:
            # Why doesn't the flashbots package have typing?
            # No flashbots specific errors?
            print(f"Simulation failed, {error=}")
            return

        replacement_uuid = str(uuid4())
        print(f"Sending bundle targeting block {current_block + 1}")
        print(f"{replacement_uuid=}")

        # Type hinting goes out the window afer this

        send_result = w3.flashbots.send_bundle(
            BUNDLE,
            target_block_number=current_block + 1,
            opts={"replacementUuid": replacement_uuid},
        )
        bundle_hash = w3.toHex(send_result.bundle_hash())
        v1_stats = w3.flashbots.get_bundle_stats(bundle_hash, current_block)
        v2_stats = w3.flashbots.get_bundle_stats_v2(bundle_hash, current_block)
        print(f"{bundle_hash=}\n{v1_stats=}\n{v2_stats=}")

        send_result.wait()
        try:
            receipts = send_result.receipts()
            print(f"Bundle was successfully mined in block {receipts[0].blockNumber}")
            break
        except TransactionNotFound:
            print(f"Bundle was not found in block {current_block + 1}, canceling")
            cancel_res = w3.flashbots.cancel_bundles(replacement_uuid)
            print(f"{cancel_res=}")


if __name__ == "__main__":
    load_dotenv()
    import utils.constants as constants

    main()
