signUpSchema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', "maxLength": 255,"minLength":3},
        'lastName': {'type': 'string', "maxLength": 255,"minLength":3},
        'email': {'type': 'string', "pattern": "[^@]+@[^@]+\.[^@]"},
        'password': {'type': 'string', "pattern": "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&+=]).*$"}
    },
    'required': ['name', 'lastName', 'email', 'password']
}