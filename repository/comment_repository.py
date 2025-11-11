from models.models import Comment, db

class CommentRepository:
    @staticmethod
    def get_by_id(id):
        return Comment.query.get_or_404(id)

    @staticmethod
    def get_active_by_post(post_id):
        return (
            Comment.query
            .filter_by(post_id=post_id, is_active=True)
            .order_by(Comment.date_time.desc())
            .all()
        )

    @staticmethod
    def create(content, user_id, post_id):
        comment = Comment(content=content, user_id=user_id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def soft_delete(comment):
        comment.is_active = False
        db.session.commit()
        return comment