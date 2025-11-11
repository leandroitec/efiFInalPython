from repository.post_repository import PostRepository
from schemas.schemas import PostSchema

#Logica de los datos de Repository (datos de las consultas a DB)
class PostService:
    
    def __init__(self):
        self.pos_repository_repository = PostRepository()

    