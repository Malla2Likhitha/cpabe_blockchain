from web3 import Web3

# Connect to local blockchain (Ganache or HTTP provider)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

contract_address = '0x147b0DF8cC33877Df54F66ba165a5Cd98281A1d1'

with open('abi.json') as f:
    contract_abi = json.load(f)

private_key = "0xbdd8d4818c1550b924a42bc84b2e9eef0cbb3131dfff196d815495a258162f78"
wallet_address = "0xac78Ca227e2c4e3aF39B5b6D6dFe66DDdf774edd"

# Load contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Set the CID value
cid_value = "QmZ5rzvqR1aGXhQJmsB68riznuR545mLZYHqk36LgqoMDG"

# Build transaction
nonce = w3.eth.get_transaction_count(wallet_address)
txn = contract.functions.setCID(cid_value).build_transaction({
    'from': wallet_address,
    'nonce': nonce,
    'gas': 200000,
    'gasPrice': Web3.to_wei('10', 'gwei')
})

# Sign and send the transaction
signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
print(f"Transaction sent: {tx_hash.hex()}")

# Wait for confirmation
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Transaction confirmed. CID set successfully.")

