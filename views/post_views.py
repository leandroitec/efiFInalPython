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
from schemas.schemas import UserSchema, RegisterSchema, LoginSchema, PostSchema
from decorators import (
    roles_required, 
    admin_or_myid_required
    )
from services.post_services import PostService
from datetime import timedelta, datetime

#-------------------------------------------------------------
#POST VIEW
#-------------------------------------------------------------
class PostAPI(MethodView):
    #---------------------------------------------
    #GET    /api/posts              # Público - listar todos los posts
    #POST   /api/posts              # Requiere autenticación (user+)
    #---------------------------------------------
    def __init__(self):
        self.user_service = PostService()
    
    #ver todos los post
    def get(self):
        posts = Post.query.filter_by(is_active=True).all()
        return PostSchema(many=True).dump(posts), 200

    @jwt_required()
    def post(self):
        try:
            data = PostSchema().load(request.json)
            user_id = get_jwt_identity()

            # Verificamos que venga una categoría válida
            categoria_id = data.get("categoria_id")
            if not categoria_id:
                return {"error": "Debe indicar una categoría"}, 400

            # Creamos el nuevo post
            new_post = Post(
                title=data['title'],
                content=data['content'],
                user_id=user_id,
                categoria_id=categoria_id,
                is_active=True
            )

            db.session.add(new_post)
            db.session.commit()

            return {"message": "Post publicado con éxito", "Post": PostSchema().dump(new_post)}, 201

        except ValidationError as error:
            return {"Error": error.messages}, 400
        except Exception as error:
            db.session.rollback()
            return {"Error": str(error)}, 500

        
    
class PostDetailAPI(MethodView):
    #---------------------------------------------
    #GET    /api/posts/<id>         # Público - ver un post específico
    #PUT    /api/posts/<id>         # Solo el autor o admin
    #DELETE /api/posts/<id>         # Solo el autor o admin
    #---------------------------------------------
    def __init__(self):
        self.user_service = PostService()

    def get(self, id):
        post = Post.query.get_or_404(id)
        if not post.is_active:
            return {"error": "el post que busca ya no esta disponible"},404
        return PostSchema().dump(post), 200
        

    def put(self):
        pass

    def delete(self):
        pass




#GET    /api/posts              # Público - listar todos los posts
#GET    /api/posts/<id>         # Público - ver un post específico
#POST   /api/posts              # Requiere autenticación (user+)
#PUT    /api/posts/<id>         # Solo el autor o admin
#DELETE /api/posts/<id>         # Solo el autor o admin


class EjAPI(MethodView):

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
    
