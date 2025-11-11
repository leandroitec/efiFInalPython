from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt
)
from functools import wraps
from models.models import Post

# decorator para verificar roles
def roles_required(*allowed_roles: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if not role or role not in allowed_roles:
                return {"Error": "acceso denegado, no tiene permisos"}
            return fn(*args, **kwargs)
        return wrapper
    return decorator

#Para admin o propia"id" requerido
def admin_or_myid_required(fn):
    @wraps (fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        current_user_id = int(get_jwt_identity()) 
        target_user_id = int(kwargs.get('id'))   #user de la ruta /user/<id<
        #logica para admin o propia id
        if claims.get("role") != "admin" and current_user_id != target_user_id:
            return {"Error": "No posee permisos"}, 403
        return fn(*args, **kwargs)
    return wrapper

#Para admin o propia "id" en post
def post_admin_myid_required(fn):
    @wraps (fn)
    def wrapper (*args, **kwargs):
        claims = get_jwt()
        current_user_id = int(get_jwt_identity()) 
        target_post_id = int(kwargs.get('id'))
        post = Post.query.get(target_post_id)
        if not post:
            return {"Error": "Post no encontrado"}, 404
        #logica
        if claims.get("role") != "admin" and current_user_id != post.user_id:
            return {"Error": "no tiene permisos"}, 403 
        return fn(*args, **kwargs)
    return wrapper
    
