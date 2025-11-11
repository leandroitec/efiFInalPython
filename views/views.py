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
from models.models import User, UserCredentials, Post, Comment, Categoria
from schemas.schemas import UserSchema, RegisterSchema, LoginSchema, CategoriaSchema, CommentSchema
from decorators import (
    roles_required, 
    admin_or_myid_required,
    comment_admin_mod_myid_required
    )
from services.user_services import UserService
from datetime import timedelta

#-------------------------------------------------------------
#USER VIEW
#-------------------------------------------------------------
#para ver todos los usuarios **CHECK**
class UserAPI(MethodView):
    #---------------------------------------------
    #GET    /api/users              # Solo admin
    #---------------------------------------------
    def __init__(self):
        self.user_service = UserService()
    
    @jwt_required()
    @roles_required("admin")
    def get(self):
        users = self.user_service.get_all_users()
        return UserSchema(many=True).dump(users)

#obtener usuarios self   **CHECK**
class UserDetailAPI(MethodView):
    #---------------------------------------------
    #GET    /api/users/<id>         # Usuario mismo o admin (usuario a uno mismo)
    #PUT    /api/users/<id>         # Usuario mismo o admin (usuario a uno mismo)
    #PATCH  /api/users/<id>/role    # Solo admin (cambiar rol)
    #DELETE /api/users/<id>         # Solo admin (desactivar)
    #---------------------------------------------
    def __init__(self):
        self.user_service = UserService()

    @jwt_required()
    @roles_required("moderator", "user", "admin")
    @admin_or_myid_required
    #obtenemos el user y roll
    def get(self, id):
        #busca y devuelve usuarios
        user = self.user_service.get_user_details(id)
        return UserSchema().dump(user), 200
    
    @jwt_required()
    @roles_required("moderator", "user", "admin")
    @admin_or_myid_required
    def put (self, id):
        try:
            updated_user = self.user_service.update_user_profile(id, request.json)
            return UserSchema().dump(updated_user), 200      
        except ValidationError as error:
            return {"errors": error.messages}, 400
        except Exception as error:
            return {"error": f"No se pudo cambiar los datos: {str(error)}"}, 400

    @jwt_required()
    @roles_required("admin")
    def patch (self, id):
        #cambiar roles
        try:
            update_user = self.user_service.change_role (id, request.json)
            return {"message": f"El rol de '{update_user.name}' actualizado a '{update_user.credential.role}'"}, 200
        except ValueError as error:
            return {"Error": str(error)}, 400
        except Exception as error:
            return {"Error": "No se pudo asignar el role"}, 400
    
    @jwt_required()
    @roles_required("admin")
    def delete (self, id):
        #eliminar usuarios  (eliminar directamente, ver borrado logico)
        try:
            self.user_service.delete_user(id)
            return {"message": f"el usuario ha sido eliminado"}, 200
        except Exception as error:
            return {"error": str(error)}, 400
    
#-------------------------------------------------------------
#AUTH VIEW
#-------------------------------------------------------------    
#registro de cuentas **CHECK**
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

#-------------------------------------------------------------
#METRICS VIEW
#-------------------------------------------------------------    
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

#-------------------------------------------------------------
#CATEGORIAS VIEW
#------------------------------------------------------------- 
# anda todo ahora
class CategoriaListAPI(MethodView):
    def get(self):
        categorias = Categoria.query.all()
        return CategoriaSchema(many=True).dump(categorias), 200

class CategoriaCreateAPI(MethodView):
    @jwt_required()
    @roles_required("admin", "moderator")
    def post(self):
        try:
            data = CategoriaSchema().load(request.get_json())
        except ValidationError as err:
            return {"errors": err.messages}, 400

        if Categoria.query.filter_by(name=data["name"]).first():
            return {"error": "Ya existe una categoría con ese nombre"}, 400

        categoria = Categoria(name=data["name"])
        db.session.add(categoria)
        db.session.commit()

        return CategoriaSchema().dump(categoria), 201

class CategoriaDetailAPI(MethodView):
    @jwt_required()
    @roles_required("moderator", "admin")
    def put(self, id):
        categoria = Categoria.query.get_or_404(id)

        json_data = request.get_json()
        if not json_data:
            return {"error": "Faltan datos"}, 400

        name = json_data.get("name", "").strip()
        if not name:
            return {"error": "El nombre no puede estar vacío"}, 400

        existente = Categoria.query.filter_by(name=name).first() 
        if existente and existente.id != id:
            return {"error": "Ya existe otra categoría con ese nombre"}, 409

        categoria.name = name
        db.session.commit()

        return CategoriaSchema().dump(categoria), 200

    @jwt_required()
    @roles_required("admin")
    def delete(self, id):
        categoria = Categoria.query.get_or_404(id)

        #borrado no logico, porque no hay activo en categoria
        db.session.delete(categoria)
        db.session.commit()

        return {"message": "Categoría elimnada correctamente"}, 200
        
#-------------------------------------------------------------
#COMMENTS VIEW
#------------------------------------------------------------- 
# probar
class PostCommentsAPI(MethodView):
    def get(self, id):
        Post.query.get_or_404(id) 
        comments = (
            Comment.query
            .filter_by(post_id=id, is_active=True)
            .order_by(Comment.date_time.desc())
            .all()
        )
        return CommentSchema(many=True).dump(comments), 200    

class CreateCommentAPI(MethodView):
    @jwt_required()
    def post(self, id):
        Post.query.get_or_404(id) 
        json_data = request.get_json()
        if not json_data:
            return {"error": "Faltan datos"}, 400
        content = json_data.get("content", "").strip()
        if not content:
            return {"error": "El comentario no puede estar vacío"}, 400
        user_id = get_jwt_identity()
        new_comment = Comment(content=content, user_id=user_id, post_id=id)

        db.session.add(new_comment)
        db.session.commit()

        return CommentSchema().dump(new_comment), 201
    
class CommentDetailAPI(MethodView):
    @jwt_required()
    @comment_admin_mod_myid_required 
    def delete(self, id, comment):
        try:
            comment = Comment.query.get_or_404(id)    
            comment.is_active = False
            db.session.commit()
            return {"message": "Comentario eliminado correctamente"}, 200
        except Exception as error:
            return {"error": str(error)}, 400




