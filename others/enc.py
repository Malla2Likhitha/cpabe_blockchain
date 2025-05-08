from charm.toolbox.pairinggroup import PairingGroup, GT
from cpabe_bsw07 import CPabe_BSW07
import requests, json, base64

def serialize_dict(group, obj, compression=True):
    if isinstance(obj, dict):
        return {k: serialize_dict(group, v, compression) for k, v in obj.items()}
    elif hasattr(obj, 'type'):  # pairing element
        return group.serialize(obj, compression).decode('utf-8')
    else:
        return obj


def encrypt():
    group = PairingGroup('SS512')
    cpabe = CPabe_BSW07(group)

    policy = '((four or three) and (three or one))'

    pk, mk = cpabe.setup()
    
    with open("attributes.txt", "r") as f:
    	attributes = f.read().strip().splitlines()

    #print(attributes)
    #attributes = ['ONE', 'TWO', 'THREE']
    sk = cpabe.keygen(pk, mk, attributes)
    
    with open("pk.txt", "w") as f:
    	f.write(str(pk))
    with open("sk.txt", "w") as f:
    	f.write(str(sk))

    msg = group.random(GT)
    ct = cpabe.encrypt(pk, msg, policy)
    
    data = {
    	"ciphertext": serialize_dict(group, ct),
    	"public_key": serialize_dict(group, pk),
    	"secret_key": serialize_dict(group, sk)
    }

    with open("abe_bundle.json", "w") as f:
        json.dump(data, f)

    print("Saved encrypted data to abe_bundle.json")
    return ct
    

if __name__ == "__main__":
    encrypt()
    
