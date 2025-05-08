# checkaccess_decrypt.py
from charm.toolbox.pairinggroup import PairingGroup, GT
from cpabe_bsw07 import CPabe_BSW07
from web3 import Web3
import requests
import json
from encrypt import encrypt

ct = encrypt()

# Setup Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.eth.default_account = w3.eth.accounts[0]

with open('abi.json') as f:
    abi = json.load(f)

contract = w3.eth.contract(address='0x147b0DF8cC33877Df54F66ba165a5Cd98281A1d1', abi=abi)
        
def deserialize_dict(group, obj, compression=True):
    if isinstance(obj, dict):
        return {k: deserialize_dict(group, v, compression) for k, v in obj.items()}
    elif isinstance(obj, str):
        return group.deserialize(obj.encode('utf-8'), compression)
    else:
        return obj


def check_access_on_chain():
    return contract.functions.checkAccess().call({'from': w3.eth.accounts[0]})

def get_cid_from_contract():
    return contract.functions.getCID().call()


def fetch_from_ipfs(cid):
    '''url = f"http://127.0.0.1:8080/ipfs/{cid}"
    res = requests.get(url)
    if res.ok:
        with open("abe_bundle.json", "wb") as f:
            f.write(res.content)
    '''
    print("Downloaded and saved as abe_bundle.json")
    '''else:
        raise Exception("IPFS fetch failed:", res.text)'''


def decrypt_from_ipfs():
    group = PairingGroup('SS512')
    cpabe = CPabe_BSW07(group)
    
    cid = get_cid_from_contract()
    fetch_from_ipfs('QmZ5rzvqR1aGXhQJmsB68riznuR545mLZYHqk36LgqoMDG')

    with open("abe_bundle.json", "r") as f:
    	data = json.load(f)
    	
    ot = deserialize_dict(group, data["ciphertext"])
    pk = deserialize_dict(group, data["public_key"])
    sk = deserialize_dict(group, data["secret_key"])


    rec_msg = cpabe.decrypt(pk, sk, ct)
    print("Recovered message:", rec_msg)

if __name__ == "__main__":
    if check_access_on_chain():
        decrypt_from_ipfs()
    else:
        print("Access denied by smart contract.")

