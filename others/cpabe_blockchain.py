from charm.toolbox.pairinggroup import PairingGroup
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from web3 import Web3
import json

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.eth.default_account = w3.eth.accounts[0]

# Load contract
with open('abi.json') as f:
    abi = json.load(f)

contract = w3.eth.contract(address='0x1a5878Dc0f977C393Dc81822928f783Ec3CB9c14', abi=abi)

def check_access_on_chain():
    return contract.functions.checkAccess().call({'from': w3.eth.accounts[0]})

def perform_cp_abe(data, user_attributes):
    group = PairingGroup('MNT224')
    cpabe = CPabe_BSW07(group)

    # Setup once
    pk, mk = cpabe.setup()

    # Define access policy separately from user attributes
    policy = '((four or three) and (three or one))'
    sk = cpabe.keygen(pk, mk, user_attributes)
    ct = cpabe.encrypt(pk, data, policy)

    try:
        pt = cpabe.decrypt(pk, sk, ct)
        print('Decryption succeeded:', pt)
        return pt
    except Exception as e:
        print("Decryption failed:", e)
        return b"Access Denied"

'''
# Main
if check_access_on_chain():
    attrs = ["Doctor", "Cardiologist"]
    data = b"Patient's medical record"
    result = perform_cp_abe(data, attrs)
    print("Access granted:", result)
else:
    print("Access denied.")
'''

attrs = ['ONE', 'TWO', 'THREE']
data = 'Patient\'s_medical_record'
result = perform_cp_abe(data, attrs)
