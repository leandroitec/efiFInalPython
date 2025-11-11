from models.models import db, Post

#Todas las consultas a DB
class PostRepository:

    # devolver todos los post
    @staticmethod
    def get_all():
        return Post.query.all()
    
    #devolver post no eliminados
    @staticmethod
    def get_all_active():
        return Post.query.filter_by(is_active=True).all()
    
    #devolver post por categoria id  **VER SI FUNCIONA**
    @staticmethod
    def get_all_catgoryfilter(categoria_id):
        return Post.query.filter_by(is_active=True, categoria_id=categoria_id).all()
    
    #deolver post por id
    @staticmethod
    def get_by_id(id):
        return Post.query.get(id)
    
    #agregar post
    @staticmethod
    def add_post(new_post):
        db.session.add(new_post)
        db.session.commit()
        return new_post
    
    #commits
    @staticmethod
    def update_post():
        db.session.commit()

    #logic delete
    @staticmethod
    def logic_delete (post):
        post.is_active = False
        db.session.commit()
        return post
    
    #delete
    @staticmethod
    def delete(post):
        db.session.delete(post)
        db.session.commit()
        return True
