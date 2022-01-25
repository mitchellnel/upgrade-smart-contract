import pytest
from brownie import Contract
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy
from scripts.helpful_scripts import encode_function_data, get_account


def test_proxy_delegate_calls():
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

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)

    assert proxy_box.getValue() == 0

    set_txn = proxy_box.setValue(3, {"from": account})
    set_txn.wait(1)

    assert proxy_box.getValue() == 3

    with pytest.raises(AttributeError):
        proxy_box.increment({"from": account})
