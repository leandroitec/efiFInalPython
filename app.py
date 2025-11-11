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
from views.views import UserRegisterAPI, AuthLoginAPI, UserAPI, UserDetailAPI, StatsAPI
from views.post_views import PostAPI, PostDetailAPI

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
app.add_url_rule(
    '/users',
    view_func=UserAPI.as_view('users_api'),
    methods=['POST', 'GET']
)

app.add_url_rule(
    '/users/<int:id>',
    view_func=UserDetailAPI.as_view('user_detail_api'),
    methods=['GET', 'PUT', 'DELETE']
)

app.add_url_rule(
    '/users/<int:id>/role',
    view_func=UserDetailAPI.as_view('user_detail_api_role'),
    methods=['PATCH']
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

#ruta metricas **VER**
app.add_url_rule(
    '/stats',
    view_func=StatsAPI.as_view('stats_api'),
    methods=['GET']
    )

app.add_url_rule(
    '/posts',
    view_func=PostAPI.as_view('post_api'),
    methods=['POST', 'GET']
)

app.add_url_rule(
    '/posts/<id>',
    view_func=PostDetailAPI.as_view('post_detail_api'),
    methods=['GET', 'PUT', 'DELETE']
)




#-------------------------------------------------------------
#RUN SERVER
#-------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

