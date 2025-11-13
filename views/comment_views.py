from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from models.models import db 

from schemas.schemas import CommentSchema
from services.comment_services import CommentService
from decorators.decorators import comment_admin_mod_myid_required

class PostCommentsAPI(MethodView):
    def __init__(self):
        self.comment_service = CommentService()

    def get(self, id):
        try:
            comments = self.comment_service.get_comments_by_post(id)
            return CommentSchema(many=True).dump(comments), 200
        except Exception as error:
            return {"errors": {"server": [str(error)]}}, 400


class CreateCommentAPI(MethodView):
    def __init__(self):
        self.comment_service = CommentService()

    @jwt_required()
    def post(self, id):
        try:
            data = request.get_json()
            if not data or "content" not in data:
                return {"errors": {"content": ["El campo 'content' es obligatorio."]}}, 400

            user_id = get_jwt_identity()
            comment = self.comment_service.create_comment(id, user_id, data)
            return CommentSchema().dump(comment), 201

        except ValidationError as error:
            return {"errors": error.messages}, 400
        except Exception as error:
            return {"errors": {"server": [f"No se pudo crear el comentario: {str(error)}"]}}, 400


class CommentDetailAPI(MethodView):
    def __init__(self):
        self.comment_service = CommentService()

    @jwt_required()
    @comment_admin_mod_myid_required
    def delete(self, id, comment):
        try:
            comment.is_active = False
            db.session.commit()
            return {"message": "Comentario eliminado correctamente"}, 200
        except Exception as error:
            return {"errors": {"server": [f"No se pudo eliminar el comentario: {str(error)}"]}}, 400


