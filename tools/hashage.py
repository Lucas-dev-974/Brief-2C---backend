from hashlib import sha512

# Hashe un mdp
def hashage(mdp:str):
    # salt = secrets.token_hex(24).encode()
    salt = b'f2937e3b3837325367839443aa583ca7b8c904029ce5a1f4' # Permet d'augementer la "force" du hashage

    mdp = mdp.encode() # string => bytes
    
    # Hashage
    mdp_hashe = sha512(salt + mdp).hexdigest()

    return mdp_hashe

print(hashage('admin'))