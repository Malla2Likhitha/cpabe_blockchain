from web3 import Web3
import json
from charm.toolbox.pairinggroup import PairingGroup
from charm.toolbox.policytree import PolicyParser
from cpabe_bsw07 import CPabe_BSW07
from encrypt import serialize_dict
from decrpyt import deserialize_dict

# Initialize Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.eth.default_account = w3.eth.accounts[0]

# Load user data from file
with open("user_data.txt", "r") as f:
    lines = f.read().strip().splitlines()
    user_attributes = [line.strip().lower() for line in lines[:-1]]
    user_to_grant = lines[-1].strip()

# Load smart contract
with open('abi.json') as f:
    abi = json.load(f)

contract_address = '0x147b0DF8cC33877Df54F66ba165a5Cd98281A1d1'
contract = w3.eth.contract(address=contract_address, abi=abi)

# Initialize pairing group and CP-ABE
group = PairingGroup('SS512')
cpabe = CPabe_BSW07(group)
util = PolicyParser()

# Load bundle and parse
with open("owner.json", "r") as f:
    daya = json.load(f)

pk = deserialize_dict(group, data["pk"])
mk = deserialize_dict(group, data["mk"])

# Load bundle and parse
with open("abe_bundle.json", "r") as f:
    bundle = json.load(f)

ct = deserialize_dict(group, bundle["ciphertext"])


# Extract and parse policy from ct
policy_str = ct['policy']
policy = util.createPolicy(policy_str)

if util.prune(policy, user_attributes) == False:
    print("Access denied: attributes do not satisfy policy.")
else:
    
    
    # Grant access on-chain
    tx_hash = contract.functions.grantAccess(user_to_grant).transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)

    sk = cpabe.keygen(pk, mk, user_attributes)

    bundle["secret_key"] = serialize_dict(group, sk)

    with open("abe_bundle.json", "w") as f:
        json.dump(bundle, f)

    print(f"Access granted to {user_to_grant}, sk updated in abe_bundle.json")
    
