from numpy import string_


signUpSchema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', "maxLength": 255, "minLength": 3},
        'lastName': {'type': 'string', "maxLength": 255, "minLength": 3},
        'email': {'type': 'string', "pattern": "[^@]+@[^@]+\.[^@]"},
        'password': {'type': 'string', "pattern": "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&+=]).*$"}
    },
    'required': ['name', 'lastName', 'email', 'password']
}

newPoem={
    'type': 'object',
    'properties': {
        'keyword': {'type': 'string', "maxLength": 255, "minLength": 3},
        'author':{'enum':['Octavio Paz','Pablo Neruda','Mario Benedetti','Garcia Lorca','Jose Luis Borges']}
    },
    'required': ['keyword','author']
}

savePoem={
    'type': 'object',
    'properties': {
        'title':{'type': 'string', "maxLength": 255, "minLength": 3},
        'keyword':{'type': 'string', "maxLength": 255, "minLength": 3},
        'poem': {'type': 'array','items':{"type":"string"},"minItems": 1},
    },
    'required': ['poem']
}
