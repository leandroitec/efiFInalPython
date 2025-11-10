from flask import request
from marshmallow import ValidationError
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt
)
from passlib.hash import bcrypt

from app import db
from models.models import User, UserCredentials, Post, Comment
from api.schemas import UserSchema, RegisterSchema, LoginSchema, PostSchema
from decorators import roles_required

from datetime import timedelta
from functools import wraps

#                                    *****MOVIDO DE LUGAR, despues eliminar*****
# decorator (para que anden todos los roles)
#def roles_required(*allowed_roles: str):
#    def decorator(fn):
#        @wraps(fn)
#        def wrapper(*args, **kwargs):
#            claims = get_jwt()
#            role = claims.get("role")
#            if not role or role not in allowed_roles:
#                return {"Error": "acceso denegado"}
#            return fn(*args, **kwargs)
#        return wrapper
#    return decorator

#para ver todos los usuarios *COMPROBAR*
    #GET    /api/users              # Solo admin
class UserAPI(MethodView):
    @jwt_required()
    @roles_required("admin")
    def get(self):
        users = User.query.all()
        return UserSchema(many=True).dump(users)

    def post(self):
        try:
            data = UserSchema().load(request.json)
            new_user = User(
                name=data.get('name'),
                email=data.get('email')
            )
            db.session.add(new_user)
            db.session.commit()
        except ValidationError as err:
            return {"Errors": f"{err.messages}"}, 400
        return UserSchema().dump(new_user), 201

# Administracion usuarios
class UserAdminAPI(MethodView):
    @jwt_required()
    @roles_required("admin")
    #Obtener los usuarios movemos abajo (USER DETAIL)
    #def get(self, id):
    #    user = User.query.get_or_404(id)
    #    return UserSchema().dump(user), 200
    
    def put(self, id):
        user = User.query.get_or_404(id)
        try: 
            data = UserSchema().load(request.json)
            user.name = data['name']
            user.email = data['email']
            db.session.commit()
            return UserSchema().dump(user), 200
        except ValidationError as err:
            return {"Error": err.messages}

    def patch(self, id):
        user = User.query.get_or_404(id)
        try: 
            data = UserSchema(partial=True).load(request.json)
            if 'name' in data:
                user.name = data.get('name')
            if 'email' in data:
                user.email = data.get('email')
            db.session.commit()
            return UserSchema().dump(user), 200
        except ValidationError as err:
            return {"Error": err.messages}
        
    def delete(self, id):
        user = User.query.get_or_404(id)
        try:
            db.session.delete(user)
            db.session.commit()
            return {"Message": "Deleted User"}, 204
        except:
            return {"Error": "No es posible borrarlo"}

#obtener usuarios self   *VER* FALTA SELF
    #GET    /api/users/<id>         # Usuario mismo o admin (usuario a uno mismo)
    #PUT    /api/users/<id>         # Usuario mismo o admin (usuario a uno mismo)
    #PATCH  /api/users/<id>/role    # Solo admin (cambiar rol)
    #DELETE /api/users/<id>         # Solo admin (desactivar)
class UserDetailAPI(MethodView):
    @jwt_required()
    @roles_required("moderator", "user", "admin")
    #obtenemos el user y roll
    def get(self, id):
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        #logica para diferenciar usuarios de admins (**puedo ponerla como decorator**)
        if claims["role"] != "admin" and current_user_id != id:
            return {"Error": "No posee permisos"}, 403
        #busca y devuelve usuarios
        user = User.query.get_or_404(id)
        return UserSchema().dump(user), 200
    
    @jwt_required()
    @roles_required("moderator", "user", "admin")
    def put (self, id):
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        #logica para diferenciar usuarios de admins (**puedo ponerla como decorator**)
        if claims["role"] != "admin" and current_user_id != id:
            return {"Error": "No posee permisos"}, 403
        #logica para actualizar usuarios
        pass

    @jwt_required()
    @roles_required("admin")
    def patch (self, id):
        #cambiar roles
        pass
    
    @jwt_required()
    @roles_required("admin")
    def delete (self, id):
        #eliminar usuarios
        pass
    
    
#registro de cuentas
class UserRegisterAPI(MethodView):
    def post(self):
        try:
            data = RegisterSchema().load(request.json)
        except ValidationError as err:
            return {"Error": err}
        
        if User.query.filter_by(email=data['email']).first():
            return {"Error": "Email en uso"}
        
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

        return {"mensaje": "Usuario creado", "user_id": UserSchema().dump(new_user)}

# autenticacion al loguearse
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
    
#para ver las metricas
# **VER** los post de last week solo lo puede ver admin
class StatsAPI(MethodView):
    @jwt_required()
    @roles_required("moderator","admin")
    def get(self):
        return {
            "total_users": User.query.count(),
            "total_posts": Post.query.count(),
            "total_comments": Comment.query.count()
        }, 200

#crear post       *VER TEMA ROLES*
class PostAPI(MethodView):

    #obtener posts
    @jwt_required()
    def get(self, post_id=None):
        # Ver todos los posts si no pasa id
        if post_id is None:
            posts = Post.query.all()
            return PostSchema(many=True).dump(posts), 200
        
        # Ver un post especifico
        post = Post.query.get_or_404(post_id)
        return PostSchema().dump(post), 200

    #crear post
    @jwt_required()
    @roles_required("user", "moderator")
    def post(self):
        try:
            data = PostSchema().load(request.json)
            user_id = get_jwt_identity()
            new_post = Post(title=data["title"], content=data["content"], user_id=user_id)
            db.session.add(new_post)
            db.session.commit()
            return PostSchema().dump(new_post), 201
        except ValidationError as err:
            return {"Error": err.messages}, 400

    #edit post
    @jwt_required()
    @roles_required("user", "moderator")
    def put(self, post_id):
        post = Post.query.get_or_404(post_id)
        user_id = get_jwt_identity()

        # Si es usuario, solo puede editar su post
        if user_id != post.user_id and "moderator" not in get_jwt_identity()["roles"]:
            return {"Error": "No autorizado"}, 403

        try:
            data = PostSchema().load(request.json)
            post.title = data["title"]
            post.content = data["content"]
            db.session.commit()
            return PostSchema().dump(post), 200
        except ValidationError as err:
            return {"Error": err.messages}, 400

    #eliminar post
    @jwt_required()
    @roles_required("user", "moderator")
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        user_id = get_jwt_identity()

        # Si es usuario, solo puede borrar su post
        if user_id != post.user_id and "moderator" not in get_jwt_identity()["roles"]:
            return {"Error": "No autorizado"}, 403

        db.session.delete(post)
        db.session.commit()
        return {"Message": "Post eliminado"}, 204
    
