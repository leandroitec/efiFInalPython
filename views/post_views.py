from flask import request
from marshmallow import ValidationError
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from schemas.schemas import PostSchema
from decorators.decorators import (
    post_admin_myid_required
    )
from services.post_services import PostService

#-------------------------------------------------------------
#POST VIEW
#-------------------------------------------------------------
class PostAPI(MethodView):
    #---------------------------------------------
    #GET    /api/posts              # Público - listar todos los posts
    #POST   /api/posts              # Requiere autenticación (user+)
    #---------------------------------------------
    def __init__(self):
        self.post_service = PostService()
    
    #ver todos los post
    def get(self):
        #posts = self.post_service.get_active_post() #**********saco filtrado para tests***************
        posts = self.post_service.get_all_post()
        return PostSchema(many=True).dump(posts)

    @jwt_required()
    def post(self):
        try:
            data = PostSchema().load(request.json)
            user_id = get_jwt_identity()
            new_post = self.post_service.new_post(data, user_id)
            return {"message" :f"post publicado con exito. Post: {PostSchema().dump(new_post)}"}, 200
        except ValidationError as error:
            return {"Error": error.messages}, 400
        except Exception as error:
            return {"Error": str(error)}, 500       


class PostDetailAPI(MethodView):
    #---------------------------------------------
    #GET    /api/posts/<id>         # Público - ver un post específico
    #PUT    /api/posts/<id>         # Solo el autor o admin
    #DELETE /api/posts/<id>         # Solo el autor o admin
    #---------------------------------------------
    def __init__(self):
        self.post_service = PostService()

    def get(self, id):
        post = self.post_service.get_by_id(id)
        if not post or not post.is_active:
            return {"error": "El post que busca ya no está disponible"}, 404
        return PostSchema().dump(post), 200
        
    @jwt_required()
    @post_admin_myid_required
    def put(self,id):
        try:
            data = PostSchema(partial=True).load(request.json)
            post = self.post_service.update_post(id, data)
            return PostSchema().dump(post), 200
        except ValidationError as error:
            return {"Error": error.messages}, 400

    @jwt_required()
    @post_admin_myid_required
    def delete(self, id):
        try:
            self.post_service.delete_post(id)
            return {"message": "Post eliminado"}, 200
        except Exception as error:
            return {"error": str(error)}, 400