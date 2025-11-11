from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from schemas.schemas import CommentSchema
from services.comment_services import CommentService
from decorators.decorators import comment_admin_mod_myid_required

class PostCommentsAPI(MethodView):
    def get(self, id):
        comments = CommentService.get_comments_by_post(id)
        return CommentSchema(many=True).dump(comments), 200


class CreateCommentAPI(MethodView):
    @jwt_required()
    def post(self, id):
        try:
            data = request.get_json()
            user_id = get_jwt_identity()
            comment = CommentService.create_comment(id, user_id, data)
            return CommentSchema().dump(comment), 201
        except ValidationError as err:
            return {"errors": err.messages}, 400


class CommentDetailAPI(MethodView):
    @jwt_required()
    @comment_admin_mod_myid_required
    def delete(self, id, comment=None):
        try:
            result = CommentService.delete_comment(id)
            return result, 200
        except ValidationError as err:
            return {"errors": err.messages}, 400