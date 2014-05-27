from formencode import Schema, validators
from pyramid_simpleform import Form

class BaseSchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = True

class LoginSchema(BaseSchema):
    username = validators.UnicodeString(max=128)
    password = validators.UnicodeString()
    
