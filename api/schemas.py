from app import db

from marshmallow import Schema, fields

from models import User

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    title = fields.Str(allow_none=True)
    date_time = fields.Date(allow_none=True)
    user = fields.Nested("UserSchema", only=["name"], dump_only=True)
    categoria = fields.Str(allow_none=True)

class Comment(Schema):
    post_id = fields.Int(dump_only=True)
    content = fields.Str(allow_none=True)
    

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    
class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(load_only=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    