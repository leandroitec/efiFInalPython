from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt
)
from functools import wraps

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