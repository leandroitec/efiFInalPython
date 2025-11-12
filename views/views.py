from flask import request
from marshmallow import ValidationError
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt

from app import db
from models.models import User, UserCredentials
from schemas.schemas import UserSchema, RegisterSchema, LoginSchema
from datetime import timedelta
    
#-------------------------------------------------------------
#AUTH VIEW
#-------------------------------------------------------------    
#registro de cuentas **CHECK**
class UserRegisterAPI(MethodView):
    def post(self):
        try:
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        
        if User.query.filter_by(email=data['email']).first():
            return {"errors": {"email": ["El email ya está en uso"]}}, 400
        
        password_hash = bcrypt.hash(data['password'])

        new_user = User(name=data["username"], email=data['email'], password=password_hash)
        db.session.add(new_user)
        db.session.flush()
        credenciales = UserCredentials(
            user_id=new_user.id,
            password_hash=password_hash,
            role=data['role']
        )
        db.session.add(credenciales)
        db.session.commit()

        return {"mensaje": "Usuario creado", "user_id": UserSchema().dump(new_user)}, 201

# autenticacion al loguearse **CHECK**
class AuthLoginAPI(MethodView):
    def post(self):
        try:
            data = LoginSchema().load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400
        user = User.query.filter_by(email=data["email"])[0]
        if not user or not user.credential:
            return {"errors": {"credentials": ["Inválidas"]}}, 401
        if not bcrypt.verify(data["password"], user.credential.password_hash):
            return {"errors": {"credentials": ["Inválidas"]}}, 401
        identity = str(user.id)
        additional_claims = {
            "id": user.id,
            "email": user.email,
            "role": user.credential.role,
            "username": user.name
        }
        token = create_access_token(
            identity=identity,
            additional_claims=additional_claims,
            # *****************cambio temporal, para facilitar el test*************************
            expires_delta=timedelta(minutes=60)
        )
        return {"access_token": token}, 200



