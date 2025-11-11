from marshmallow import ValidationError
from repository.comment_repository import CommentRepository
from repository.post_repository import PostRepository  # para verificar que exista el post

class CommentService:
    @staticmethod
    def get_comments_by_post(post_id):
        # validar que el post exista
        PostRepository.get_by_id(post_id)
        return CommentRepository.get_active_by_post(post_id)

    @staticmethod
    def create_comment(post_id, user_id, data):
        PostRepository.get_by_id(post_id)
        content = data.get("content", "").strip()

        if not content:
            raise ValidationError({"content": "El comentario no puede estar vacío"})

        comment = CommentRepository.create(content, user_id, post_id)
        return comment

    @staticmethod
    def delete_comment(id):
        comment = CommentRepository.get_by_id(id)
        if not comment.is_active:
            raise ValidationError({"error": "El comentario ya fue eliminado"})
        CommentRepository.soft_delete(comment)
        return {"message": "Comentario eliminado correctamente"}