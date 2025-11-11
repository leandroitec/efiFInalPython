from flask import request
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from marshmallow import ValidationError
from services.categorie_services import CategoriaService
from schemas.schemas import CategoriaSchema
from decorators.decorators import roles_required

class CategoriaListAPI(MethodView):
    def get(self):
        categorias = CategoriaService.list_all()
        return CategoriaSchema(many=True).dump(categorias), 200

class CategoriaCreateAPI(MethodView):
    @jwt_required()
    @roles_required("admin", "moderator")
    def post(self):
        try:
            data = request.get_json()
            categoria = CategoriaService.create(data)
            return CategoriaSchema().dump(categoria), 201
        except ValidationError as err:
            return {"errors": err.messages}, 400

class CategoriaDetailAPI(MethodView):
    @jwt_required()
    @roles_required("moderator", "admin")
    def put(self, id):
        try:
            data = request.get_json()
            categoria = CategoriaService.update(id, data)
            return CategoriaSchema().dump(categoria), 200
        except ValidationError as err:
            return {"errors": err.messages}, 400

    @jwt_required()
    @roles_required("admin")
    def delete(self, id):
        result = CategoriaService.delete(id)
        return result, 200