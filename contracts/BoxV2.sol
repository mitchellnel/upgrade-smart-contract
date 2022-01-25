// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BoxV2 {
    uint256 private value;

    event ValueChanged(uint256 newValue);

    function getValue() public view returns (uint256) {
        return value;
    }

    function setValue(uint256 newValue) public {
        value = newValue;
        emit ValueChanged(newValue);
    }

    function increment() public {
        value += 1;
        emit ValueChanged(value);
    }
}
