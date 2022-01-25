from brownie import accounts, config, network, Contract
import eth_utils
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None, id=None):
    if index is not None:
        return accounts[index]
    elif id is not None:
        return accounts.load(id)
    elif (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


# initialiser = box.store, 1
def encode_function_data(initialiser=None, *args):
    """Encodes the function call so we can work with an initializer.
    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.
        args (Any, optional):
        The arguments to pass to the initializer function
    Returns:
        [bytes]: Return the encoded bytes.
    """
    if len(args) == 0 or not initialiser:
        return eth_utils.to_bytes(hexstr="0x")
    else:
        return initialiser.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initialiser=None,
    *args
):
    if proxy_admin_contract:
        if initialiser:
            encoded_function_call = encode_function_data(initialiser, *args)

            txn = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_call,
                {"from": account},
            )
        else:
            txn = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
    elif initialiser:
        encoded_function_call = encode_function_data(initialiser, *args)
        txn = proxy.upgradeToAndCall(
            new_implementation_address, encoded_function_call, {"from": account}
        )
    else:
        txn = proxy.upgradeTo(new_implementation_address, {"from": account})

    return txn
