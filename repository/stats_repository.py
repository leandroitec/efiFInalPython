from models.models import User, Post, Comment, db
from datetime import datetime, timedelta

class StatsRepository:
    @staticmethod
    def count_users():
        return User.query.count()

    @staticmethod
    def count_posts():
        return Post.query.count()

    @staticmethod
    def count_comments():
        return Comment.query.count()

    @staticmethod
    def count_posts_last_week():
        last_week = datetime.utcnow() - timedelta(days=7)
        return Post.query.filter(Post.date_time >= last_week).count()

    @staticmethod
    def count_comments_last_week():
        last_week = datetime.utcnow() - timedelta(days=7)
        return Comment.query.filter(Comment.date_time >= last_week).count()