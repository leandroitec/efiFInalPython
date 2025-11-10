from app import db

from marshmallow import Schema, fields

from models.models import User

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    date_time = fields.DateTime(dump_only=True)
    # Relaciones fk
    user_id = fields.Int(load_only=True)
    autor = fields.Nested("UserSchema", only=["name"], dump_only=True)
    categoria_id = fields.Int(load_only=True)
    categoria = fields.Nested("CategoriaSchema", only=["nombre"], dump_only=True)
    #boolean para eliminado logico
    is_active = fields.Bool(dump_only=True)

#comentarios schema
class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    date_time = fields.DateTime(dump_only=True)
    # Relaciones fk
    user_id = fields.Int(load_only=True)
    autor = fields.Nested("UserSchema", only=["name"], dump_only=True)
    post_id = fields.Int(load_only=True)
    post = fields.Nested("PostSchema", only=["title"], dump_only=True)
    #boolean borrado logico
    is_active = fields.Bool(dump_only=True)
    

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

#schema de categoria
class CategoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    #para que en thunder te tire lo post de cada ctegoria
    posts = fields.Nested("PostSchema", many=True, exclude=("categoria",), dump_only=True)
    