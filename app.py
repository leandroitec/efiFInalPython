#-------------------------------------------------------------
#IMPORTS
#-------------------------------------------------------------
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
#import db
from models.models import (
    db,
    User,
    Post,
)
from flask_migrate import Migrate
#import schemas
from views.post_views import PostAPI, PostDetailAPI
from views.categorie_view import CategoriaCreateAPI, CategoriaListAPI, CategoriaDetailAPI
from views.comment_views import CommentDetailAPI, PostCommentsAPI, CreateCommentAPI
from views.stast_views import StatsAPI
from views.views import UserRegisterAPI, AuthLoginAPI
from views.user_view import UserAPI, UserDetailAPI
from flask_cors import CORS

#-------------------------------------------------------------
#INICIA FLASK, SQL, ETC
#-------------------------------------------------------------
app = Flask(__name__)

# Configuración del Frontend de React
REACT_ORIGIN = "http://localhost:5173" 

# Inicializa CORS, permitiendo solo el origen de React
CORS(app, resources={r"/*": {"origins": REACT_ORIGIN}})

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

#ruta metricas 
app.add_url_rule(
    '/stats',
    view_func=StatsAPI.as_view('stats_api'),
    methods=['GET']
    )
# posteos
app.add_url_rule(
    '/posts',
    view_func=PostAPI.as_view('post_api'),
    methods=['POST', 'GET']
)

app.add_url_rule(
    '/posts/<int:id>',
    view_func=PostDetailAPI.as_view('post_detail_api'),
    methods=['GET', 'PUT', 'DELETE']
)

#categorias
app.add_url_rule(
    "/categories",
    view_func=CategoriaListAPI.as_view("categoria_list"),
    methods=["GET"]
)

app.add_url_rule(
    "/categories",
    view_func=CategoriaCreateAPI.as_view("categoria_create"),
    methods=["POST"]
)

app.add_url_rule(
    "/categories/<int:id>",
    view_func=CategoriaDetailAPI.as_view("categoria_detail"),
    methods=["PUT", "DELETE"]
)

#comments
app.add_url_rule(
    "/posts/<int:id>/comments",
    view_func=PostCommentsAPI.as_view("post_comments"),
    methods=["GET"]
)

app.add_url_rule(
    "/posts/<int:id>/comments",
    view_func=CreateCommentAPI.as_view("create_comment"),
    methods=["POST"]
)

app.add_url_rule(
    "/comments/<int:id>",
    view_func=CommentDetailAPI.as_view("comment_detail"),
    methods=["DELETE"]
)

#-------------------------------------------------------------
#RUN SERVER
#-------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

