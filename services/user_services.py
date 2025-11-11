from repository.user_repository import UserRepository
from schemas.schemas import UserSchema

#Logica de los datos de Repository (datos de las consultas a DB)
class UserService:
    
    def __init__(self):
        self.user_repository = UserRepository()

    # Obtener todos los usuarios    
    def get_all_users(self):
        return self.user_repository.get_all()
    
    #obtiene el usuario por id o 404
    def get_user_details(self, user_id):
        user = self.user_repository.get_by_id_or_404(user_id)
        return user
    
    #Obtiene el usuario, y lo actualiza con el json
    def update_user_profile(self, user_id, user_data):
        data=UserSchema(partial=True).load(user_data)
        user = self.user_repository.get_by_id_or_404(user_id)
        updated_user = self.user_repository.update_user(user, data)     
        return updated_user
    
    #cambia rol
    def change_role (self, user_id, role_data):
        new_role = role_data.get("role")
        if new_role not in ["user", "moderator", "admin"]:
            raise ValueError(f"Rol inválido: '{new_role}'. Los roles permitidos son: user, moderator, admin.")
        user = self.user_repository.get_by_id_or_404(user_id)
        update_user = self.user_repository.change_rol(user, new_role)
        return update_user
    
    #borrar usuario
    def delete_user (self, user_id):
        self.user_repository.delete_user(user_id)
        return True
    
    #Logci delete post
    def softdelete_user(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("El usuario no existe")
        self.user_repository.logic_delete(user)
        return True