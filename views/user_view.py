from flask import request
from marshmallow import ValidationError
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
)
from schemas.schemas import UserSchema
from decorators.decorators import (
    roles_required, 
    admin_or_myid_required
    )
from services.user_services import UserService

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
        try:
            self.user_service.softdelete_user(id)
            return {"message": f"el usuario ha sido eliminado"}, 200
        except Exception as error:
            return {"error": str(error)}, 400