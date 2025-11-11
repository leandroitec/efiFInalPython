from models.models import db, User, UserCredentials

#Todas las consultas a DB
class UserRepository:

    #consulta que devuelve todo lo de USER
    @staticmethod
    def get_all():
        return User.query.all()
    
    #consulta devuelve usuarios por id
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    #consulta devuelve usuario busca usuario por id o devuelve 404    
    @staticmethod
    def get_by_id_or_404(user_id):
        """Busca un usuario por ID y levanta 404 si no existe."""
        # Se mantiene get_or_404 porque es una función específica del ORM
        return User.query.get_or_404(user_id)
    
    #cambia los datos de la db
    @staticmethod
    def update_user(user, data):
        
        if "username" in data:
            user.name = data["username"]
        if "email" in data:
            user.email = data["email"]
        db.session.commit()
        return user
    
    # actualiza user_credentials (rol)
    @staticmethod
    def change_rol(user, new_role):
        user.credential.role = new_role
        db.session.commit()
        return user
    
    # borrado total de usuario y credenciales
    @staticmethod
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user.credential)
        db.session.delete(user)
        db.session.commit()
        return True
    
    #logic delete
    @staticmethod
    def logic_delete (user):
        user.is_active = False
        db.session.commit()
        return user