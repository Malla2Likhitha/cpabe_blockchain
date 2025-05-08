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

    msg = group.random(GT)
    ct = cpabe.encrypt(pk, msg, policy)
    
    data = {
    	"ciphertext": serialize_dict(group, ct),
    	"public_key": serialize_dict(group, pk),
    	"secret_key": 0
    }

    with open("abe_bundle.json", "w") as f:
        json.dump(data, f)
    print("Saved encrypted data to abe_bundle.json")
    
    data2 = {
    	"mk": serialize_dict(group, mk),
    	"pk": serialize_dict(group, pk)
    }

    with open("owner.json", "w") as f:
        json.dump(data2, f)

    return ct
    

if __name__ == "__main__":
    encrypt()
    
