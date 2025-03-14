#help.py
import hashlib, json
senha = "String a calcular"
hash = hashlib.sha256(senha.encode()).hexdigest()
print(hash)


with open('usuarios.json', 'r') as f:
    print(json.load(f))