#-------------------------------------------------------------
#IMPORTS
#-------------------------------------------------------------
from flask import Flask, request
from flask_jwt_extended import JWTManager
#import db
from models.models import (
    db,
    User,
    Post,
)
from flask_migrate import Migrate
#import schemas
from api.views import UserRegisterAPI, AuthLoginAPI, UserAPI, UserDetailAPI, StatsAPI, UserAdminAPI

#-------------------------------------------------------------
#INICIA FLASK, SQL, ETC
#-------------------------------------------------------------
app = Flask(__name__)

#cambiar esto si tenes usuario y contraseña, //usuario:contraseña@host:@localhost/pyIIefi_db"
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://root:@localhost/pyIIefi_final"
)
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'cualquier-cosa'

jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)

#-------------------------------------------------------------
#RUTAS/ENDPOINT
#-------------------------------------------------------------
#solo el admin
app.add_url_rule(
    '/users',
    view_func=UserAPI.as_view('users_api'),
    methods=['POST', 'GET']
)

#UserDetailAPI todos los roles
# *VER* , usuario, mod solo ven sl propio, ademin ve todos
app.add_url_rule(
    '/users/<int:id>',
    view_func=UserDetailAPI.as_view('user_detail_api'),
    methods=['GET', 'PUT', 'PATCH', 'DELETE']
)

# Public
app.add_url_rule(
    '/login',
    view_func=AuthLoginAPI.as_view('user_user_api'),
    methods=['POST']
)

#Public
app.add_url_rule(
    '/register',
    view_func=UserRegisterAPI.as_view('user_register_api'),
    methods=['POST']
)

#ruta metricas (moderadires/admin)  *VER SCHEMA*
app.add_url_rule(
    '/stats',
    view_func=StatsAPI.as_view('stats_api'),
    methods=['GET']
    )


#-------------------------------------------------------------
#RUN SERVER
#-------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

