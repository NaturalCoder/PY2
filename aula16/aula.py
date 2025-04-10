import json

a = '''
{
    "nome": "Maria",
    "idade": 25,
    "ativo": true,
    "telefones": ["11987654321", "1133334444"]
}
'''
b = {
    "nome": "Maria",
    "idade": 25,
    "ativo": True,
    "telefones": ["11987654321", "1133334444"]
}

f = [ "ficha1"
     , "ficha2"
     ]

#c = json.loads(a)
f.append({"ficha3":3 })


print(f)
print(type(f))
