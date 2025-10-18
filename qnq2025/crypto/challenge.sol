// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import "Timelock.sol";

contract Challenge {
    address public immutable PLAYER;
    Timelock public immutable CONTRACT;

    bool private solved;

    constructor(address player, address _contract) public {
        PLAYER = player;
        
        CONTRACT = Timelock(payable(_contract));
    }

    function solve() external {
        require(CONTRACT.balanceOf(PLAYER) == 0, "COINS_NOT_SPENT");
        solved = true;
    }

    function isSolved() external view returns (bool) {
        return solved;
    }
}
