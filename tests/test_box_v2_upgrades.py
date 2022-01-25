import pytest
from brownie import Contract, exceptions
from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy
from scripts.helpful_scripts import encode_function_data, get_account, upgrade


def test_proxy_upgrades():
    account = get_account()

    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})

    box_encoded_initialiser = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initialiser,
        {"from": account, "gas_limit": 1_000_000},
    )

    # deploy BoxV2
    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})

    upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)

    assert proxy_box.getValue() == 0

    inc_txn = proxy_box.increment({"from": account})
    inc_txn.wait(1)

    assert proxy_box.getValue() == 1
