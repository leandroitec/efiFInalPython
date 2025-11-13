from flask import request
from marshmallow import ValidationError
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from schemas.schemas import UserSchema
from decorators.decorators import (
    roles_required, 
    admin_or_myid_required
)
from services.user_services import UserService

#-------------------------------------------------------------
# USER VIEW
#-------------------------------------------------------------
# Para ver todos los usuarios **CHECK**
class UserAPI(MethodView):
    def __init__(self):
        self.user_service = UserService()
    
    @jwt_required()
    @roles_required("admin")
    def get(self):
        try:
            users = self.user_service.get_all_users()
            return UserSchema(many=True).dump(users), 200
        except Exception as error:
            return {"errors": {"server": [str(error)]}}, 400


# Obtener usuario por ID, editar, borrar, etc. **CHECK**
class UserDetailAPI(MethodView):
    def __init__(self):
        self.user_service = UserService()

    @jwt_required()
    @roles_required("moderator", "user", "admin")
    @admin_or_myid_required
    def get(self, id):
        try:
            user = self.user_service.get_user_details(id)
            return UserSchema().dump(user), 200
        except Exception as error:
            return {"errors": {"server": [str(error)]}}, 400
    
    @jwt_required()
    @roles_required("moderator", "user", "admin")
    @admin_or_myid_required
    def put(self, id):
        try:
            updated_user = self.user_service.update_user_profile(id, request.json)
            return UserSchema().dump(updated_user), 200      
        except ValidationError as error:
            # Marshmallow ya devuelve el formato {"campo": ["mensaje"]}
            return {"errors": error.messages}, 400
        except Exception as error:
            return {"errors": {"server": [f"No se pudo cambiar los datos: {str(error)}"]}}, 400

    @jwt_required()
    @roles_required("admin")
    def patch(self, id):
        try:
            update_user = self.user_service.change_role(id, request.json)
            return {"message": f"El rol de '{update_user.name}' actualizado a '{update_user.credential.role}'"}, 200
        except ValueError as error:
            return {"errors": {"role": [str(error)]}}, 400
        except Exception as error:
            return {"errors": {"server": ["No se pudo asignar el rol"]}}, 400
    
    @jwt_required()
    @roles_required("admin")
    def delete(self, id):
        try:
            self.user_service.softdelete_user(id)
            return {"message": "El usuario ha sido eliminado"}, 200
        except Exception as error:
            return {"errors": {"server": [str(error)]}}, 400
