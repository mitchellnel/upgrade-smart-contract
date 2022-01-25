from brownie import config, network, Contract
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy
from scripts.helpful_scripts import encode_function_data, get_account
from scripts.upgrade_box import upgrade_box


def deploy_box():
    account = get_account()

    print(f"Deploying Box contract to {network.show_active()} ...")
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"... Done! Box deployed to {box.address}\n")

    print("Setting Box's value to 3 ...")
    set_txn = box.setValue(3, {"from": account})
    set_txn.wait(1)
    print("... Done! Value set.\n")

    print("Getting Box's value ...")
    get_val = box.getValue({"from": account})
    print(f"... Done! We got a value of {get_val} from Box.\n")

    # hooking up a proxy to our implementation contract
    print("Deploying Proxy Admin ...")
    proxy_admin = ProxyAdmin.deploy({"from": account})
    print(f"... Done! Proxy deployed to {proxy_admin.address}\n")

    # encoding a function to be our initialiser
    initialiser = box.setValue, 1  # function_to_call, first_parameter
    box_encoded_initialiser_function = encode_function_data(initialiser)

    print("Deploying the Proxy Contract ...")
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initialiser_function,
        {"from": account, "gas_limit": 1_000_000},
    )
    print(f"... Done! Proxy Contract deployed to {proxy.address}\n")

    # assigning ABI to a proxy so we can call implementation contract functions on the proxy
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)

    print("Using proxy to get value from Box ...")
    set_txn = proxy_box.setValue(33, {"from": account})
    set_txn.wait(1)
    get_val = proxy_box.getValue()
    print(f"... Done! We got a value of {get_val} using our proxy for Box.\n")

    upgrade_box()


def main():
    deploy_box()
