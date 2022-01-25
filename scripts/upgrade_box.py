from brownie import config, network, Contract
from brownie import BoxV2, ProxyAdmin, TransparentUpgradeableProxy
from scripts.helpful_scripts import get_account, upgrade


def upgrade_box():
    account = get_account()

    proxy_admin = ProxyAdmin[-1]
    proxy = TransparentUpgradeableProxy[-1]

    box_v2 = BoxV2.deploy({"from": account})

    print("Upgrading proxy ...")
    upgrade_txn = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    print(f"... Done! Proxy upgraded.\n")

    # assigning ABI to a proxy so we can call implementation contract functions on the proxy
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    print("Using proxy to implement value of 33 to 34 on BoxV2 ...")
    inc_txn = proxy_box.increment({"from": account})
    inc_txn.wait(1)
    get_val = proxy_box.getValue()
    print(f"... Done! We got a value of {get_val} using our proxy for BoxV2.\n")


def main():
    upgrade_box()
